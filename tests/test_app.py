import unittest

from app import create_app


class CatalogTestCase(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Monkey D. Luffy", response.data)

    def test_search(self):
        response = self.client.get("/?q=brook")
        self.assertIn(b"Brook", response.data)
        self.assertNotIn(b"Roronoa Zoro", response.data)

    def test_character_detail(self):
        response = self.client.get("/personagem/brook")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Soul King", response.data)

    def test_missing_character(self):
        self.assertEqual(self.client.get("/personagem/inexistente").status_code, 404)


if __name__ == "__main__":
    unittest.main()
