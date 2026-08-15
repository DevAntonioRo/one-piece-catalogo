from copy import deepcopy
from secrets import token_hex

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

from data import CHARACTERS, CREWS, TOWER, crew_members, get_character
from game.combat import resolve_attack, resolve_enemy_attack

TEAM_BUDGET = 3200
ENEMIES = {floor["enemy"] for floor in TOWER}
PLAYABLE = {character["slug"] for character in CHARACTERS if character["slug"] not in ENEMIES}


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=token_hex(24))
    if test_config:
        app.config.update(test_config)

    @app.template_filter("berries")
    def format_berries(value):
        return f"{value:,.0f}".replace(",", ".")

    @app.context_processor
    def template_globals():
        return {"tower_state": session.get("tower"), "team_budget": TEAM_BUDGET}

    @app.get("/")
    def index():
        query = request.args.get("q", "").strip().lower()
        crew = request.args.get("crew", "").strip()
        characters = CHARACTERS
        if query:
            characters = [c for c in characters if query in c["name"].lower() or query in c["epithet"].lower()]
        if crew:
            characters = [c for c in characters if c["crew"] == crew]
        return render_template("index.html", characters=characters, crews=sorted({c["crew"] for c in CHARACTERS}), selected_crew=crew, query=request.args.get("q", "").strip())

    @app.get("/personagem/<slug>")
    def character_detail(slug):
        character = get_character(slug)
        if not character:
            abort(404)
        return render_template("detail.html", character=character)

    @app.get("/tripulacoes")
    def crews():
        enriched = [{**crew, "members": crew_members(crew["name"])} for crew in CREWS]
        return render_template("crews.html", crews=enriched)

    @app.route("/jogo/equipe", methods=["GET", "POST"])
    def team_builder():
        playable = [c for c in CHARACTERS if c["slug"] in PLAYABLE]
        if request.method == "POST":
            selected = list(dict.fromkeys(request.form.getlist("characters")))
            chosen = [get_character(slug) for slug in selected if slug in PLAYABLE]
            cost = sum(c["game"]["cost"] for c in chosen)
            if len(chosen) != 3:
                flash("Escolha exatamente três personagens.", "error")
            elif cost > TEAM_BUDGET:
                flash(f"Sua equipe custa {cost} créditos e ultrapassa o limite de {TEAM_BUDGET}.", "error")
            else:
                session["tower"] = new_tower_state(chosen)
                return redirect(url_for("tower"))
        return render_template("team.html", characters=playable, budget=TEAM_BUDGET)

    @app.get("/jogo/torre")
    def tower():
        state = session.get("tower")
        if not state:
            return redirect(url_for("team_builder"))
        team = [get_character(slug) for slug in state["team"]]
        return render_template("tower.html", state=state, team=team, floors=TOWER)

    @app.route("/jogo/batalha", methods=["GET", "POST"])
    def battle():
        state = session.get("tower")
        if not state:
            return redirect(url_for("team_builder"))
        if state["floor"] >= len(TOWER):
            return redirect(url_for("tower"))
        floor = TOWER[state["floor"]]
        enemy = get_character(floor["enemy"])
        if not state.get("battle"):
            state["battle"] = {"enemy_hp": enemy["game"]["hp"], "enemy_energy": enemy["game"]["energy"], "enemy_statuses": [], "tangible": 0, "log": [f"{enemy['name']} surgiu em {floor['name']}."]}
            session["tower"] = state
        if request.method == "POST" and state["battle"]["enemy_hp"] > 0:
            play_turn(state, enemy, request.form)
            session["tower"] = state
        team = [get_character(slug) for slug in state["team"]]
        alive = any(state["fighters"][member]["hp"] > 0 for member in state["team"])
        return render_template("battle.html", state=state, team=team, enemy=enemy, floor=floor, alive=alive)

    @app.post("/jogo/avancar")
    def advance_floor():
        state = session.get("tower")
        if not state:
            return redirect(url_for("team_builder"))
        if not state.get("battle") or state["battle"]["enemy_hp"] > 0:
            abort(400)
        state["berries"] += TOWER[state["floor"]]["reward"]
        state["floor"] += 1
        state["battle"] = None
        session["tower"] = state
        return redirect(url_for("tower"))

    @app.post("/jogo/loja")
    def shop():
        state = session.get("tower")
        if not state:
            return redirect(url_for("team_builder"))
        item = request.form.get("item")
        prices = {"heal": 900, "energy": 650, "training": 1500}
        if item not in prices or state["berries"] < prices[item]:
            flash("Berries insuficientes ou item inválido.", "error")
            return redirect(url_for("tower"))
        state["berries"] -= prices[item]
        if item == "heal":
            for slug in state["team"]:
                state["fighters"][slug]["hp"] = get_character(slug)["game"]["hp"]
        elif item == "energy":
            for slug in state["team"]:
                state["fighters"][slug]["energy"] = get_character(slug)["game"]["energy"]
        else:
            state["strength_bonus"] += 6
        session["tower"] = state
        flash("Compra realizada. Sua equipe está mais preparada.", "success")
        return redirect(url_for("tower"))

    @app.post("/jogo/reiniciar")
    def reset_game():
        session.pop("tower", None)
        return redirect(url_for("team_builder"))

    @app.get("/api/personagens")
    def api_characters():
        return {"characters": CHARACTERS, "count": len(CHARACTERS)}

    return app


def new_tower_state(team):
    return {
        "team": [c["slug"] for c in team], "floor": 0, "berries": 0,
        "strength_bonus": 0, "battle": None, "resources": {"water": 2, "seastone": 1},
        "fighters": {c["slug"]: {"hp": c["game"]["hp"], "energy": c["game"]["energy"], "stance": "guarded", "statuses": []} for c in team},
    }


def play_turn(state, enemy, form):
    slug = form.get("fighter")
    if slug not in state["team"] or state["fighters"][slug]["hp"] <= 0:
        flash("Escolha um integrante disponível.", "error")
        return
    fighter = deepcopy(get_character(slug))
    fighter["game"]["strength"] += state.get("strength_bonus", 0)
    fighter_state = state["fighters"][slug]
    battle = state["battle"]
    enemy_state = {"hp": battle["enemy_hp"], "energy": battle["enemy_energy"], "statuses": battle["enemy_statuses"], "tangible": battle["tangible"]}
    action = {
        "intensity": form.get("intensity"), "body_part": form.get("body_part"),
        "approach": form.get("approach"), "stance": form.get("stance"),
        "use_haki": form.get("use_haki") == "on",
        "element": form.get("element") or fighter["game"]["element"],
    }
    selected_resource = form.get("element")
    if selected_resource in state["resources"]:
        if state["resources"][selected_resource] <= 0:
            flash("Esse recurso tático acabou.", "error")
            return
        state["resources"][selected_resource] -= 1
    result = resolve_attack(fighter, enemy, action, fighter_state, enemy_state)
    fighter_state["energy"] = max(0, fighter_state["energy"] - result.energy_cost)
    fighter_state["stance"] = action["stance"]
    battle["enemy_hp"] = max(0, battle["enemy_hp"] - result.damage)
    battle["tangible"] = enemy_state.get("tangible", 0)
    if result.status and result.status not in battle["enemy_statuses"]:
        battle["enemy_statuses"].append(result.status)
    battle["log"].append(f"{fighter['name']}: {result.message} Dano: {result.damage}.")
    if battle["enemy_hp"] <= 0:
        battle["log"].append(f"Vitória! {enemy['name']} foi derrotado.")
        return
    damage, message = resolve_enemy_attack(enemy, fighter, enemy_state, fighter_state)
    fighter_state["hp"] = max(0, fighter_state["hp"] - damage)
    battle["enemy_statuses"] = enemy_state["statuses"]
    battle["log"].append(message)
    if battle["tangible"]:
        battle["tangible"] -= 1
    if all(state["fighters"][member]["hp"] <= 0 for member in state["team"]):
        battle["log"].append("Sua equipe foi derrotada. Reinicie a expedição e tente outra estratégia.")
    battle["log"] = battle["log"][-30:]


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
