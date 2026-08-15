import unittest

from app import create_app


class CatalogTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "SECRET_KEY": "test"})
        self.client = self.app.test_client()

    def test_home_and_wiki_pages(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Monkey D. Luffy", response.data)
        self.assertEqual(self.client.get("/tripulacoes").status_code, 200)

    def test_search(self):
        response = self.client.get("/?q=brook")
        self.assertIn(b"Brook", response.data)
        self.assertNotIn(b"Roronoa Zoro", response.data)

    def test_character_detail_and_missing(self):
        response = self.client.get("/personagem/crocodile")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Suna Suna no Mi", response.data)
        self.assertEqual(self.client.get("/personagem/inexistente").status_code, 404)

    def test_team_requires_three_members(self):
        response = self.client.post("/jogo/equipe", data={"characters": ["brook"]}, follow_redirects=True)
        self.assertIn("exatamente três".encode(), response.data)

    def test_valid_team_starts_tower(self):
        response = self.client.post("/jogo/equipe", data={"characters": ["nami", "brook", "nico-robin"]}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Grand Line Tower", response.data)

    def test_battle_page_and_turn(self):
        self.client.post("/jogo/equipe", data={"characters": ["nami", "brook", "nico-robin"]})
        response = self.client.get("/jogo/batalha")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Rob Lucci", response.data)
        response = self.client.post("/jogo/batalha", data={
            "skill_nami": "thunderbolt", "approach_nami": "feint", "body_nami": "torso", "stance_nami": "guarded",
            "skill_brook": "soul_freeze", "approach_brook": "direct", "body_brook": "legs", "stance_brook": "guarded",
            "skill_nico-robin": "clutch", "approach_nico-robin": "direct", "body_nico-robin": "arms", "stance_nico-robin": "guarded",
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("DIÁRIO DE COMBATE".encode(), response.data)

    def test_api(self):
        payload = self.client.get("/api/personagens").get_json()
        self.assertEqual(payload["count"], 33)


if __name__ == "__main__":
    unittest.main()
