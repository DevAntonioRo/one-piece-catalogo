from copy import deepcopy
from random import Random
from secrets import token_hex

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

from data import CHARACTERS, CREWS, SKILLS, SYNERGIES, TOWER, crew_members, get_character, get_skill
from game.combat import initiative_actions, resolve_action, tick_state

TEAM_BUDGET = 4200


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=token_hex(24))
    if test_config: app.config.update(test_config)

    @app.template_filter("berries")
    def berries(value): return f"{value:,.0f}".replace(",", ".")

    @app.context_processor
    def globals_for_templates():
        return {"tower_state": session.get("tower"), "team_budget": TEAM_BUDGET, "skills": SKILLS}

    @app.get("/")
    def index():
        query = request.args.get("q", "").strip().lower()
        crew = request.args.get("crew", "").strip()
        characters = CHARACTERS
        if query: characters = [c for c in characters if query in c["name"].lower() or query in c["epithet"].lower()]
        if crew: characters = [c for c in characters if c["crew"] == crew]
        return render_template("index.html", characters=characters, crews=sorted({c["crew"] for c in CHARACTERS}), selected_crew=crew, query=request.args.get("q", "").strip())

    @app.get("/personagem/<slug>")
    def character_detail(slug):
        character = get_character(slug)
        if not character: abort(404)
        return render_template("detail.html", character=character, specials=[get_skill(skill) for skill in character["skills"]])

    @app.get("/tripulacoes")
    def crews():
        return render_template("crews.html", crews=[{**crew, "members": crew_members(crew["name"])} for crew in CREWS])

    @app.route("/jogo/equipe", methods=["GET", "POST"])
    def team_builder():
        playable = [c for c in CHARACTERS if c["playable"]]
        if request.method == "POST":
            selected = list(dict.fromkeys(request.form.getlist("characters")))
            chosen = [get_character(slug) for slug in selected if get_character(slug) and get_character(slug)["playable"]]
            cost = sum(c["game"]["cost"] for c in chosen)
            if len(chosen) != 3: flash("Escolha exatamente três personagens.", "error")
            elif cost > TEAM_BUDGET: flash(f"Equipe de {cost} créditos ultrapassa o limite de {TEAM_BUDGET}.", "error")
            else:
                session["tower"] = new_tower_state(chosen)
                return redirect(url_for("tower"))
        return render_template("team.html", characters=playable, budget=TEAM_BUDGET)

    @app.get("/jogo/torre")
    def tower():
        state = session.get("tower")
        if not state: return redirect(url_for("team_builder"))
        return render_template("tower.html", state=state, team=[get_character(s) for s in state["team"]], floors=TOWER)

    @app.route("/jogo/batalha", methods=["GET", "POST"])
    def battle():
        state = session.get("tower")
        if not state: return redirect(url_for("team_builder"))
        if state["floor"] >= len(TOWER): return redirect(url_for("tower"))
        floor = TOWER[state["floor"]]
        enemy = get_character(floor["enemy"])
        if not state.get("battle"):
            state["battle"] = new_battle_state(enemy, floor)
        if request.method == "POST" and state["battle"]["enemy"]["hp"] > 0:
            play_round(state, enemy, request.form)
        session["tower"] = state
        team = [get_character(s) for s in state["team"]]
        alive = any(state["fighters"][s]["hp"] > 0 for s in state["team"])
        return render_template("battle.html", state=state, team=team, enemy=enemy, floor=floor, alive=alive)

    @app.post("/jogo/avancar")
    def advance_floor():
        state = session.get("tower")
        if not state: return redirect(url_for("team_builder"))
        if not state.get("battle") or state["battle"]["enemy"]["hp"] > 0: abort(400)
        state["berries"] += TOWER[state["floor"]]["reward"]
        state["floor"] += 1; state["battle"] = None
        session["tower"] = state
        return redirect(url_for("tower"))

    @app.post("/jogo/loja")
    def shop():
        state = session.get("tower")
        if not state: return redirect(url_for("team_builder"))
        item = request.form.get("item"); prices = {"heal": 1000, "energy": 750, "training": 1700}
        if item not in prices or state["berries"] < prices[item]:
            flash("Berries insuficientes ou item inválido.", "error"); return redirect(url_for("tower"))
        state["berries"] -= prices[item]
        for slug in state["team"]:
            if item == "heal": state["fighters"][slug]["hp"] = get_character(slug)["game"]["hp"]
            elif item == "energy": state["fighters"][slug]["energy"] = get_character(slug)["game"]["energy"]
        if item == "training": state["strength_bonus"] += 5
        session["tower"] = state; flash("Melhoria aplicada à equipe.", "success")
        return redirect(url_for("tower"))

    @app.post("/jogo/reiniciar")
    def reset_game():
        session.pop("tower", None); return redirect(url_for("team_builder"))

    @app.get("/api/personagens")
    def api_characters(): return {"characters": CHARACTERS, "count": len(CHARACTERS)}

    return app


def new_tower_state(team):
    slugs = [c["slug"] for c in team]
    synergy = SYNERGIES.get(frozenset(slugs))
    return {"team": slugs, "floor": 0, "berries": 0, "strength_bonus": 0,
            "synergy": synergy, "battle": None,
            "fighters": {c["slug"]: fighter_state(c) for c in team}}


def fighter_state(character):
    return {"hp": character["game"]["hp"], "energy": character["game"]["energy"],
            "stance": "guarded", "statuses": [], "cooldowns": {}, "initiative": 0,
            "silenced": 0, "tangible": 0}


def new_battle_state(enemy, floor):
    return {"enemy": fighter_state(enemy), "round": 0,
            "log": [f"{enemy['name']} bloqueia o caminho em {floor['name']}. Planeje as três ações."]}


def with_team_bonuses(character, state):
    result = deepcopy(character)
    result["game"]["strength"] += state.get("strength_bonus", 0)
    synergy = state.get("synergy")
    if synergy:
        stat = synergy["stat"]; result["game"][stat] = round(result["game"][stat] * (1 + synergy["bonus"]))
    return result


def play_round(state, enemy, form, rng=None):
    rng = rng or Random()
    battle = state["battle"]; enemy_state = battle["enemy"]
    battle["round"] += 1
    queue = []
    for slug in state["team"]:
        fs = state["fighters"][slug]
        if fs["hp"] <= 0: continue
        character = with_team_bonuses(get_character(slug), state)
        skill_id = form.get(f"skill_{slug}", "basic")
        if skill_id not in {"basic", *character["skills"]}: skill_id = "basic"
        command = {"skill": skill_id, "body_part": form.get(f"body_{slug}", "torso"),
                   "stance": form.get(f"stance_{slug}", "guarded"),
                   "approach": form.get(f"approach_{slug}", "direct"),
                   "use_haki": form.get(f"haki_{slug}") == "on"}
        actions, fs["initiative"] = initiative_actions(character["game"]["speed"], fs["initiative"])
        for number in range(actions): queue.append((character["game"]["speed"], "player", slug, command, number > 0))

    enemy_actions, enemy_state["initiative"] = initiative_actions(enemy["game"]["speed"], enemy_state["initiative"])
    for number in range(enemy_actions): queue.append((enemy["game"]["speed"], "enemy", enemy["slug"], None, number > 0))
    queue.sort(key=lambda item: item[0] + rng.random(), reverse=True)
    battle["log"].append(f"— Rodada {battle['round']} — Ordem definida pela velocidade.")

    for _, side, slug, command, bonus in queue:
        if enemy_state["hp"] <= 0: break
        if side == "player":
            fs = state["fighters"][slug]
            if fs["hp"] <= 0: continue
            character = with_team_bonuses(get_character(slug), state)
            blocking = next((s for s in ("stunned","frozen","petrified","restrained","controlled") if s in fs["statuses"]), None)
            if blocking:
                fs["statuses"].remove(blocking); battle["log"].append(f"{character['name']} perdeu a ação por estar {blocking}."); continue
            result = resolve_action(character, enemy, command, fs, enemy_state, rng, .62 if bonus else 1)
            fs["energy"] = max(0, fs["energy"] - result.energy_cost); fs["stance"] = command["stance"]
            if result.energy_cost and command["skill"] != "basic": fs["cooldowns"][command["skill"]] = get_skill(command["skill"])["cooldown"] + 1
            enemy_state["hp"] = max(0, enemy_state["hp"] - result.damage)
            if result.status in {"regenerate", "heal_team"}:
                weakest_slug = min(state["team"], key=lambda s: state["fighters"][s]["hp"] / get_character(s)["game"]["hp"])
                weakest = state["fighters"][weakest_slug]
                heal = 220 if result.status == "heal_team" else 160
                weakest["hp"] = min(get_character(weakest_slug)["game"]["hp"], weakest["hp"] + heal)
                battle["log"].append(f"{get_character(weakest_slug)['name']} recuperou {heal} de vida.")
                result.status = None
            if character.get("passive") == "weather_boost" and command["skill"] == "thunderbolt":
                for ally in state["team"]: state["fighters"][ally]["initiative"] += 12
                battle["log"].append("Nami alterou os ventos: +12 de iniciativa para a equipe.")
            apply_effect(result.status, fs, enemy_state)
            battle["log"].append(f"{character['name']} {result.message}{' em ação extra' if bonus else ''}.")
        else:
            blocking = next((s for s in ("stunned","frozen","petrified","restrained","controlled") if s in enemy_state["statuses"]), None)
            if blocking:
                enemy_state["statuses"].remove(blocking); battle["log"].append(f"{enemy['name']} perdeu a ação por estar {blocking}."); continue
            alive = [s for s in state["team"] if state["fighters"][s]["hp"] > 0]
            if not alive: break
            target_slug = max(alive, key=lambda s: state["fighters"][s]["hp"])
            target = with_team_bonuses(get_character(target_slug), state); target_state = state["fighters"][target_slug]
            command = {"skill": enemy["skill"] if not enemy_state["cooldowns"].get(enemy["skill"], 0) else "basic", "body_part": "torso", "stance": "aggressive", "approach": "direct", "use_haki": "armament" in enemy["haki"]}
            result = resolve_action(enemy, target, command, enemy_state, target_state, rng, .62 if bonus else 1)
            enemy_state["energy"] = max(0, enemy_state["energy"] - result.energy_cost)
            if result.energy_cost and command["skill"] != "basic": enemy_state["cooldowns"][command["skill"]] = get_skill(command["skill"])["cooldown"] + 1
            target_state["hp"] = max(0, target_state["hp"] - result.damage)
            apply_effect(result.status, enemy_state, target_state)
            battle["log"].append(f"{enemy['name']} {result.message} em {target['name']}{' em ação extra' if bonus else ''}.")

    for slug in state["team"]: tick_state(state["fighters"][slug])
    tick_state(enemy_state)
    if enemy_state["hp"] <= 0: battle["log"].append(f"Vitória! {enemy['name']} foi derrotado.")
    elif not any(state["fighters"][s]["hp"] > 0 for s in state["team"]): battle["log"].append("Toda a equipe foi derrotada.")
    battle["log"] = battle["log"][-40:]


def apply_effect(effect, attacker_state, defender_state):
    if not effect: return
    if effect == "regenerate": attacker_state["hp"] += 120; return
    if effect == "silenced": defender_state["silenced"] = 1; return
    if effect not in defender_state["statuses"]: defender_state["statuses"].append(effect)


app = create_app()
if __name__ == "__main__": app.run(debug=True)
