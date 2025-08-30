from typing import Dict, List, Any
import re

class EntityNormalizer:
    """Normalize extracted entities to standard formats"""
    
    def __init__(self):
        # Dictionary for species normalization
        self.species_map = {
            "жираф": "giraffe",
            "слон": "elephant",
            "лев": "lion",
            "тигр": "tiger",
            "медведь": "bear",
            "волк": "wolf",
            "лиса": "fox",
            # Add more as needed
        }
        
        # Dictionary for food normalization
        self.food_map = {
            "люцерна": "alfalfa",
            "сено": "hay",
            "мясо": "meat",
            "рыба": "fish",
            "фрукты": "fruits",
            "овощи": "vegetables",
            # Add more as needed
        }
        
        # Dictionary for behavior normalization
        self.behavior_map = {
            "спокойное": "calm",
            "агрессивное": "aggressive",
            "игривое": "playful",
            "вялое": "lethargic",
            # Add more as needed
        }
        
    def normalize_entities(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize all entities to standard formats"""
        normalized = entities.copy()
        
        # Normalize animal species
        if "animal" in normalized and "species" in normalized["animal"]:
            species = normalized["animal"]["species"].lower()
            if species in self.species_map:
                normalized["animal"]["species"] = self.species_map[species]
        
        # Normalize food names
        if "feeding" in normalized and "food" in normalized["feeding"]:
            food = normalized["feeding"]["food"].lower()
            if food in self.food_map:
                normalized["feeding"]["food"] = self.food_map[food]
        
        # Normalize behavior types
        if "behavior" in normalized and "type" in normalized["behavior"]:
            behavior = normalized["behavior"]["type"].lower()
            if behavior in self.behavior_map:
                normalized["behavior"]["type"] = self.behavior_map[behavior]
        
        # Convert temperature from string to float if needed
        if "vitals" in normalized and "temperature_c" in normalized["vitals"]:
            temp = normalized["vitals"]["temperature_c"]
            if isinstance(temp, str):
                normalized["vitals"]["temperature_c"] = float(temp.replace(',', '.'))
        
        # Convert weight from string to float if needed
        if "vitals" in normalized and "weight_kg" in normalized["vitals"]:
            weight = normalized["vitals"]["weight_kg"]
            if isinstance(weight, str):
                normalized["vitals"]["weight_kg"] = float(weight.replace(',', '.'))
        
        # Convert feeding amount from string to float if needed
        if "feeding" in normalized and "amount_g" in normalized["feeding"]:
            amount = normalized["feeding"]["amount_g"]
            if isinstance(amount, str):
                normalized["feeding"]["amount_g"] = float(amount.replace(',', '.'))
        
        return normalized
    
    def validate_entities(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Validate entities against defined rules"""
        validated = entities.copy()
        
        # Validate temperature range (normal for mammals is 35-40°C)
        if "vitals" in validated and "temperature_c" in validated["vitals"]:
            temp = validated["vitals"]["temperature_c"]
            if temp < 30 or temp > 45:
                # Temperature outside normal range, add alert
                if "alert" not in validated:
                    validated["alert"] = {}
                validated["alert"]["severity"] = "warning"
                validated["alert"]["message"] = f"Abnormal temperature: {temp}°C"
        
        # Validate weight (assuming reasonable range for zoo animals)
        if "vitals" in validated and "weight_kg" in validated["vitals"]:
            weight = validated["vitals"]["weight_kg"]
            if weight < 0.1 or weight > 10000:
                # Weight outside reasonable range, add alert
                if "alert" not in validated:
                    validated["alert"] = {}
                validated["alert"]["severity"] = "warning"
                validated["alert"]["message"] = f"Abnormal weight: {weight}kg"
        
        return validated