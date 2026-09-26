import unittest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

class LegalEaseApiTests(unittest.TestCase):
    def test_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "running")

    def test_health(self):
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_generate_validation(self):
        response = client.post("/generate", json={
            "document_type": "",
            "parties": "A",
            "terms": "B",
            "effective_date": "2026-09-25"
        })
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()
