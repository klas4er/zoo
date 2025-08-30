import unittest
from engine.ner import EntityExtractor
from engine.normalization import EntityNormalizer

class TestEntityExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = EntityExtractor()
        self.normalizer = EntityNormalizer()
    
    def test_animal_extraction(self):
        text = "Самка жирафа Жужа ела 700 грамм люцерны"
        entities = self.extractor.extract_entities(text)
        
        # Check that animal entity is extracted
        self.assertIn("animal", entities)
        self.assertIn("name", entities["animal"])
        self.assertEqual(entities["animal"]["name"], "Жужа")
    
    def test_temperature_extraction(self):
        text = "температура 37.8"
        entities = self.extractor.extract_entities(text)
        
        # Check that vitals entity with temperature is extracted
        self.assertIn("vitals", entities)
        self.assertIn("temperature_c", entities["vitals"])
        self.assertEqual(entities["vitals"]["temperature_c"], 37.8)
    
    def test_weight_extraction(self):
        text = "вес 850 кг"
        entities = self.extractor.extract_entities(text)
        
        # Check that vitals entity with weight is extracted
        self.assertIn("vitals", entities)
        self.assertIn("weight_kg", entities["vitals"])
        self.assertEqual(entities["vitals"]["weight_kg"], 850.0)
    
    def test_feeding_extraction(self):
        text = "ела 700 грамм люцерны"
        entities = self.extractor.extract_entities(text)
        
        # Check that feeding entity is extracted
        self.assertIn("feeding", entities)
        self.assertIn("amount_g", entities["feeding"])
        self.assertEqual(entities["feeding"]["amount_g"], 700.0)
    
    def test_entity_normalization(self):
        entities = {
            "animal": {"species": "жираф"},
            "feeding": {"food": "люцерна"},
            "behavior": {"type": "спокойное"}
        }
        
        normalized = self.normalizer.normalize_entities(entities)
        
        # Check normalization
        self.assertEqual(normalized["animal"]["species"], "giraffe")
        self.assertEqual(normalized["feeding"]["food"], "alfalfa")
        self.assertEqual(normalized["behavior"]["type"], "calm")
    
    def test_entity_validation(self):
        entities = {
            "vitals": {"temperature_c": 42.0, "weight_kg": 850.0}
        }
        
        validated = self.normalizer.validate_entities(entities)
        
        # Check that high temperature generates an alert
        self.assertIn("alert", validated)
        self.assertEqual(validated["alert"]["severity"], "warning")

if __name__ == "__main__":
    unittest.main()