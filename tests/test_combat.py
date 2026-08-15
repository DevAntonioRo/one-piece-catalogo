import unittest
from random import Random

from data import get_character
from game.combat import initiative_actions, resolve_action


class CombatRulesTestCase(unittest.TestCase):
    def state(self, character):
        return {"hp": character["game"]["hp"], "energy": 999, "statuses": [], "cooldowns": {}, "initiative": 0, "silenced": 0, "tangible": 0, "stance": "guarded"}

    def test_cutting_damage_is_zero_against_buggy(self):
        zoro, buggy = get_character("roronoa-zoro"), get_character("buggy")
        result = resolve_action(zoro, buggy, {"skill":"precision_cut","body_part":"torso"}, self.state(zoro), self.state(buggy), Random(1))
        self.assertEqual(result.damage, 0)
        self.assertIn("imune", result.message)

    def test_normal_attack_cannot_hit_logia(self):
        zoro, crocodile = get_character("roronoa-zoro"), get_character("crocodile")
        result = resolve_action(zoro, crocodile, {"skill":"basic","body_part":"torso"}, self.state(zoro), self.state(crocodile), Random(1))
        self.assertEqual(result.damage, 0)

    def test_haki_can_hit_logia(self):
        zoro, crocodile = get_character("roronoa-zoro"), get_character("crocodile")
        result = resolve_action(zoro, crocodile, {"skill":"basic","body_part":"torso","use_haki":True}, self.state(zoro), self.state(crocodile), Random(1))
        self.assertGreater(result.damage, 0)

    def test_law_ignores_defense(self):
        law, kaido = get_character("trafalgar-law"), get_character("kaido")
        result = resolve_action(law, kaido, {"skill":"room","body_part":"torso"}, self.state(law), self.state(kaido), Random(1))
        self.assertGreater(result.damage, 100)

    def test_fast_character_earns_bonus_action_sooner(self):
        fast_actions, fast_meter = initiative_actions(98, 98)
        slow_actions, slow_meter = initiative_actions(65, 65)
        self.assertEqual(fast_actions, 2)
        self.assertEqual(slow_actions, 1)
        self.assertLess(fast_meter, 180)
        self.assertLess(slow_meter, 180)

    def test_zoro_and_sanji_are_close_but_specialized(self):
        zoro, sanji = get_character("roronoa-zoro"), get_character("sanji")
        self.assertLessEqual(abs(zoro["game"]["strength"] - sanji["game"]["strength"]), 5)
        self.assertGreater(zoro["game"]["strength"], sanji["game"]["strength"])
        self.assertGreater(sanji["game"]["speed"], zoro["game"]["speed"])
        self.assertGreater(sanji["game"]["defense"], zoro["game"]["defense"])

    def test_legendary_characters_are_not_recruitable(self):
        self.assertFalse(get_character("shanks")["playable"])
        self.assertFalse(get_character("whitebeard")["playable"])
        self.assertFalse(get_character("blackbeard")["playable"])


if __name__ == "__main__": unittest.main()
