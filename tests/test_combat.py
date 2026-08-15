import unittest
from random import Random

from data import get_character
from game.combat import resolve_attack


class CombatRulesTestCase(unittest.TestCase):
    def setUp(self):
        self.zoro = get_character("roronoa-zoro")
        self.nami = get_character("nami")
        self.crocodile = get_character("crocodile")
        self.attacker_state = {"energy": 999, "statuses": []}
        self.defender_state = {"tangible": 0, "statuses": []}
        self.base_action = {"intensity": "balanced", "body_part": "torso", "approach": "direct", "stance": "guarded"}

    def test_normal_attack_cannot_hit_logia(self):
        result = resolve_attack(self.zoro, self.crocodile, self.base_action, self.attacker_state, self.defender_state, Random(1))
        self.assertEqual(result.damage, 0)
        self.assertIn("Logia", result.message)

    def test_armament_haki_can_hit_logia(self):
        result = resolve_attack(self.zoro, self.crocodile, {**self.base_action, "use_haki": True}, self.attacker_state, self.defender_state, Random(1))
        self.assertGreater(result.damage, 0)

    def test_water_makes_crocodile_tangible(self):
        result = resolve_attack(self.nami, self.crocodile, {**self.base_action, "element": "water"}, self.attacker_state, self.defender_state, Random(1))
        self.assertTrue(result.made_tangible)
        self.assertEqual(self.defender_state["tangible"], 2)

    def test_character_without_haki_cannot_use_it(self):
        result = resolve_attack(self.nami, self.crocodile, {**self.base_action, "use_haki": True}, self.attacker_state, self.defender_state, Random(1))
        self.assertEqual(result.energy_cost, 0)
        self.assertIn("não domina", result.message)


if __name__ == "__main__":
    unittest.main()
