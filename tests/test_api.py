import unittest
from fastapi.testclient import TestClient
from backend.main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
    
    def test_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})
    
    def test_entity_config(self):
        config = {
            "entities": [
                {"name": "animal", "fields": ["name", "species", "id"], "required": ["species"]},
                {"name": "behavior", "fields": ["type", "intensity", "duration_sec"]},
                {"name": "vitals", "fields": ["temperature_c", "weight_kg"], "validators": {"temperature_c": ">= 25 & <= 45"}},
                {"name": "feeding", "fields": ["food", "amount_g", "time"]},
                {"name": "relations", "fields": ["animal_id", "relation_type"]},
                {"name": "location", "fields": ["enclosure", "zone"]},
                {"name": "alert", "fields": ["severity", "message"]}
            ],
            "rules": {
                "dates": "регэкспы/парсеры дат",
                "numbers": "регэкспы для температур/весов/количеств"
            }
        }
        
        response = self.client.post("/api/entities/config", json=config)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), config)

if __name__ == "__main__":
    unittest.main()