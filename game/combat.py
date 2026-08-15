from dataclasses import dataclass
from random import Random

INTENSITY = {
    "quick": {"damage": .72, "energy": 24, "accuracy": .96},
    "balanced": {"damage": 1.0, "energy": 42, "accuracy": .86},
    "heavy": {"damage": 1.38, "energy": 68, "accuracy": .68},
}
BODY_PARTS = {
    "head": {"damage": 1.35, "accuracy": .72, "effect": "stunned"},
    "torso": {"damage": 1.0, "accuracy": 1.0, "effect": None},
    "arms": {"damage": .82, "accuracy": .91, "effect": "weakened"},
    "legs": {"damage": .78, "accuracy": .90, "effect": "slowed"},
}


@dataclass
class CombatResult:
    damage: int
    energy_cost: int
    hit: bool
    message: str
    status: str | None = None
    made_tangible: bool = False


def resolve_attack(attacker, defender, action, attacker_state, defender_state, rng=None):
    """Resolve propriedades do ataque sem exceções baseadas no nome do atacante."""
    rng = rng or Random()
    intensity = INTENSITY.get(action.get("intensity"), INTENSITY["balanced"])
    body = BODY_PARTS.get(action.get("body_part"), BODY_PARTS["torso"])
    use_haki = action.get("use_haki", False)
    element = action.get("element") or attacker["game"].get("element")
    energy_cost = intensity["energy"] + (22 if use_haki else 0)
    if attacker_state["energy"] < energy_cost:
        return CombatResult(0, 0, False, "Energia insuficiente para executar essa ação.")
    if use_haki and "armament" not in attacker.get("haki", []):
        return CombatResult(0, 0, False, f"{attacker['name']} não domina Haki do Armamento.")

    made_tangible = element in defender.get("weaknesses", [])
    if defender.get("fruit_type") == "logia" and not defender_state.get("tangible") and not use_haki and not made_tangible:
        return CombatResult(0, energy_cost, False, f"O ataque atravessou {defender['name']}. Uma Logia exige Haki do Armamento ou uma fraqueza compatível.")
    if made_tangible:
        defender_state["tangible"] = 2

    defender_speed = defender["game"]["speed"] * (.78 if "slowed" in defender_state.get("statuses", []) else 1)
    accuracy = intensity["accuracy"] * body["accuracy"] + (attacker["game"]["speed"] - defender_speed) / 450
    if action.get("approach") == "feint":
        accuracy += attacker["game"]["technique"] / 800
    if rng.random() > max(.22, min(.97, accuracy)):
        return CombatResult(0, energy_cost, False, f"{defender['name']} leu a aproximação e evitou o golpe.", made_tangible=made_tangible)

    attack_power = attacker["game"]["strength"] * .62 + attacker["game"]["technique"] * .38
    base = max(12, attack_power * 1.75 - defender["game"]["defense"])
    modifier = intensity["damage"] * body["damage"]
    if use_haki:
        modifier *= 1 + attacker["game"]["haki_level"] * .11
    if made_tangible:
        modifier *= 1.18
    if action.get("stance") == "aggressive":
        modifier *= 1.12
    damage = max(1, round(base * modifier * rng.uniform(.92, 1.08)))
    status = body["effect"] if body["effect"] and rng.random() < .22 + attacker["game"]["technique"] / 500 else None
    return CombatResult(damage, energy_cost, True, "Ataque conectado com sucesso.", status, made_tangible)


def resolve_enemy_attack(enemy, target, enemy_state, target_state, rng=None):
    rng = rng or Random()
    if "stunned" in enemy_state.get("statuses", []):
        enemy_state["statuses"].remove("stunned")
        return 0, f"{enemy['name']} perdeu o turno após ser atordoado."
    multiplier = 1.25 if enemy_state["hp"] < enemy["game"]["hp"] * .35 else rng.uniform(.82, 1.08)
    base = max(16, enemy["game"]["strength"] * 1.45 - target["game"]["defense"] * .68)
    if target_state.get("stance") == "guarded":
        base *= .74
    elif target_state.get("stance") == "aggressive":
        base *= 1.18
    damage = round(base * multiplier)
    return damage, f"{enemy['name']} contra-atacou e causou {damage} de dano em {target['name']}."
