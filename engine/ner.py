import re
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    PER,
    NamesExtractor,
    Doc
)
import spacy
from typing import Dict, List, Any
from datetime import datetime

class EntityExtractor:
    def __init__(self):
        """Initialize NER models and rules"""
        # Natasha initialization
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        
        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.syntax_parser = NewsSyntaxParser(self.emb)
        self.ner_tagger = NewsNERTagger(self.emb)
        
        self.names_extractor = NamesExtractor(self.emb)
        
        # spaCy initialization
        self.nlp = spacy.load("ru_core_news_sm")
        
        # Custom regex rules
        self.rules = {
            "temperature": r"(?i)(температура|температура тела)\s*(\d+[,\.]?\d*)\s*(°?[cс])",
            "weight": r"(?i)(вес|масса)\s*(\d+[,\.]?\d*)\s*(кг|kg)",
            "food_amount": r"(?i)(\d+[,\.]?\d*)\s*(грамм|г|kg|кг)",
            "date": r"(?i)(\d{1,2}[.\-]\d{1,2}[.\-]\d{4}|\d{1,2}[.\-]\d{1,2})"
        }
        
        # Entity types we're interested in
        self.entity_types = {
            "animal": ["species", "name", "id"],
            "behavior": ["type", "intensity", "duration_sec"],
            "vitals": ["temperature_c", "weight_kg"],
            "feeding": ["food", "amount_g", "time"],
            "relations": ["animal_id", "relation_type"],
            "location": ["enclosure", "zone"],
            "alert": ["severity", "message"]
        }
        
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract all entities from text"""
        entities = {}
        
        # Use Natasha for general NER
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.parse_syntax(self.syntax_parser)
        doc.tag_ner(self.ner_tagger)
        
        # Normalize morphological tags
        for token in doc.tokens:
            token.lemmatize(self.morph_vocab)
        
        # Normalize NER spans
        for span in doc.spans:
            span.normalize(self.morph_vocab)
        
        # Extract named entities
        for span in doc.spans:
            if span.type == "PER":  # Person names might be animal names
                if "animal" not in entities:
                    entities["animal"] = {}
                entities["animal"]["name"] = span.normal
        
        # Use spaCy for additional processing
        spacy_doc = self.nlp(text)
        
        # Extract entities with spaCy
        for ent in spacy_doc.ents:
            if ent.label_ == "PERSON":  # Might be animal names
                if "animal" not in entities:
                    entities["animal"] = {}
                entities["animal"]["name"] = ent.text
        
        # Apply regex rules
        entities.update(self._apply_regex_rules(text))
        
        return entities
    
    def _apply_regex_rules(self, text: str) -> Dict[str, Any]:
        """Apply custom regex rules to extract entities"""
        entities = {}
        
        # Temperature extraction
        temp_match = re.search(self.rules["temperature"], text)
        if temp_match:
            if "vitals" not in entities:
                entities["vitals"] = {}
            # Replace comma with dot for proper float conversion
            temp_value = temp_match.group(2).replace(',', '.')
            entities["vitals"]["temperature_c"] = float(temp_value)
        
        # Weight extraction
        weight_match = re.search(self.rules["weight"], text)
        if weight_match:
            if "vitals" not in entities:
                entities["vitals"] = {}
            weight_value = weight_match.group(2).replace(',', '.')
            entities["vitals"]["weight_kg"] = float(weight_value)
        
        # Food amount extraction
        food_match = re.search(self.rules["food_amount"], text)
        if food_match:
            if "feeding" not in entities:
                entities["feeding"] = {}
            amount_value = food_match.group(1).replace(',', '.')
            entities["feeding"]["amount_g"] = float(amount_value)
        
        # Date extraction
        date_match = re.search(self.rules["date"], text)
        if date_match:
            try:
                # Try to parse the date
                date_str = date_match.group(1)
                if len(date_str.split('.')) == 3 or len(date_str.split('-')) == 3:
                    # Full date with year
                    date_obj = datetime.strptime(date_str, "%d.%m.%Y") if '.' in date_str else datetime.strptime(date_str, "%d-%m-%Y")
                else:
                    # Date without year
                    date_obj = datetime.strptime(date_str, "%d.%m") if '.' in date_str else datetime.strptime(date_str, "%d-%m")
                
                if "observation" not in entities:
                    entities["observation"] = {}
                entities["observation"]["date"] = date_obj.isoformat()
            except ValueError:
                # If we can't parse the date, skip it
                pass
        
        return entities