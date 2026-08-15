from dataclasses import dataclass
from random import Random

from data import get_skill

BODY_PARTS = {
    "head": {"damage": 1.28, "accuracy": .72, "effect": "stunned"},
    "torso": {"damage": 1.0, "accuracy": 1.0, "effect": None},
    "arms": {"damage": .84, "accuracy": .90, "effect": "weakened"},
    "legs": {"damage": .80, "accuracy": .90, "effect": "slowed"},
}


@dataclass
class CombatResult:
    damage: int
    energy_cost: int
    hit: bool
    message: str
    status: str | None = None
    made_tangible: bool = False


def initiative_actions(speed, meter):
    """Todos agem uma vez; o excedente acumulado concede ações extras."""
    meter += speed
    extra = 0
    while meter >= 180:
        extra += 1
        meter -= 100
    return 1 + extra, meter


def resolve_action(attacker, defender, command, attacker_state, defender_state, rng=None, bonus_scale=1.0):
    rng = rng or Random()
    skill = get_skill(command.get("skill", "basic"))
    body = BODY_PARTS.get(command.get("body_part"), BODY_PARTS["torso"])
    use_haki = command.get("use_haki", False)
    damage_type = skill.get("damage_type", attacker.get("damage_type", "physical"))
    energy_cost = skill["energy"] + (18 if use_haki else 0)

    if attacker_state["energy"] < energy_cost:
        return CombatResult(0, 0, False, "não tinha energia para completar a ação")
    if attacker_state.get("silenced") and skill != get_skill("basic"):
        return CombatResult(0, 0, False, "teve a habilidade bloqueada pela escuridão")
    if use_haki and "armament" not in attacker.get("haki", []):
        return CombatResult(0, 0, False, "não domina Haki do Armamento")
    if attacker_state.get("cooldowns", {}).get(command.get("skill"), 0) > 0:
        return CombatResult(0, 0, False, "tentou usar uma habilidade ainda em recarga")

    made_tangible = damage_type in defender.get("weaknesses", [])
    if damage_type in defender.get("immunities", []):
        return CombatResult(0, energy_cost, False, f"não causou dano: {defender['name']} é imune a {damage_type}")
    if defender.get("fruit_type") == "logia" and not defender_state.get("tangible") and not use_haki and not made_tangible:
        return CombatResult(0, energy_cost, False, "não atingiu o corpo real da Logia")
    if made_tangible:
        defender_state["tangible"] = 2

    attack_strength = attacker["game"]["strength"]
    attack_technique = attacker["game"]["technique"]
    if attacker.get("passive") == "gear_five" and attacker_state["hp"] <= attacker["game"]["hp"] * .2:
        attack_strength *= 1.5
        attack_technique *= 1.5

    target_speed = defender["game"]["speed"] * (.80 if "slowed" in defender_state.get("statuses", []) else 1)
    accuracy = .82 * body["accuracy"] + (attacker["game"]["speed"] - target_speed) / 500
    if command.get("approach") == "feint": accuracy += attack_technique / 850
    if rng.random() > max(.30, min(.98, accuracy)):
        return CombatResult(0, energy_cost, False, "errou após o alvo antecipar a trajetória", made_tangible=made_tangible)

    mitigation = .68 * (1 - skill.get("ignore_defense", 0))
    stance_factor = 1.15 if defender_state.get("stance") == "guarded" else (.88 if defender_state.get("stance") == "aggressive" else 1)
    defense = defender["game"]["defense"] * stance_factor * (0.78 if "guard_break" in defender_state.get("statuses", []) else 1)
    raw = attack_strength * skill["power"] * 2.15 - defense * mitigation
    critical_chance = max(.04, (attack_technique - 65) / 260)
    critical = rng.random() < critical_chance
    modifier = body["damage"] * bonus_scale * (1.5 if critical else 1)
    if use_haki: modifier *= 1 + len(attacker.get("haki", [])) * .06
    if made_tangible: modifier *= 1.15
    if defender.get("passive") == "double_damage_taken": modifier *= 2
    damage = max(1, round(raw * modifier * rng.uniform(.94, 1.06)))

    effect = skill.get("effect") or (body["effect"] if rng.random() < attack_technique / 330 else None)
    if defender.get("passive") == "exoskeleton": damage = round(damage * .85)
    if defender.get("passive") == "regeneration": damage = round(damage * .82)
    message = f"usou {skill['name']} e causou {damage} de dano"
    if critical: message += " (CRÍTICO)"
    return CombatResult(damage, energy_cost, True, message, effect, made_tangible)


def tick_state(state):
    for skill, turns in list(state.get("cooldowns", {}).items()):
        state["cooldowns"][skill] = max(0, turns - 1)
    state["silenced"] = max(0, state.get("silenced", 0) - 1)
    if state.get("tangible"): state["tangible"] -= 1
    if "burn" in state.get("statuses", []): state["hp"] = max(0, state["hp"] - 24)
    if "bleed" in state.get("statuses", []): state["hp"] = max(0, state["hp"] - 18)
