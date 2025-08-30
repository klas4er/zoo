from sqlalchemy.orm import Session
from models import Animal, Observation, ObservationEntity, Relation
from schemas import AnimalCreate, ObservationCreate, ObservationEntityCreate
from typing import List, Optional
from datetime import datetime

class AnimalRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_animal(self, animal_id: int) -> Optional[Animal]:
        return self.db.query(Animal).filter(Animal.id == animal_id).first()
    
    def get_animals(self, skip: int = 0, limit: int = 100) -> List[Animal]:
        return self.db.query(Animal).offset(skip).limit(limit).all()
    
    def create_animal(self, animal: AnimalCreate) -> Animal:
        db_animal = Animal(
            species=animal.species,
            name=animal.name,
            tags=animal.tags
        )
        self.db.add(db_animal)
        self.db.commit()
        self.db.refresh(db_animal)
        return db_animal

class ObservationRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_observation(self, observation_id: int) -> Optional[Observation]:
        return self.db.query(Observation).filter(Observation.id == observation_id).first()
    
    def get_observations(self, animal_id: Optional[int] = None, watcher_id: Optional[int] = None, 
                         start_date: Optional[datetime] = None, end_date: Optional[datetime] = None,
                         skip: int = 0, limit: int = 100) -> List[Observation]:
        query = self.db.query(Observation)
        
        if animal_id:
            query = query.filter(Observation.animal_id == animal_id)
        
        if watcher_id:
            query = query.filter(Observation.watcher_id == watcher_id)
        
        if start_date:
            query = query.filter(Observation.ts >= start_date)
        
        if end_date:
            query = query.filter(Observation.ts <= end_date)
        
        return query.offset(skip).limit(limit).all()
    
    def create_observation(self, observation: dict) -> Observation:
        # Convert dict to Observation object
        db_observation = Observation(
            animal_id=observation["animal_id"],
            watcher_id=observation["watcher_id"],
            raw_text=observation["raw_text"],
            confidence=observation["confidence"]
        )
        self.db.add(db_observation)
        self.db.commit()
        self.db.refresh(db_observation)
        return db_observation

class ObservationEntityRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_entities_by_observation(self, observation_id: int) -> List[ObservationEntity]:
        return self.db.query(ObservationEntity).filter(ObservationEntity.observation_id == observation_id).all()
    
    def create_observation_entity(self, entity: dict) -> ObservationEntity:
        # Convert dict to ObservationEntity object
        db_entity = ObservationEntity(
            observation_id=entity["observation_id"],
            type=entity["type"],
            payload_json=entity["payload_json"]
        )
        self.db.add(db_entity)
        self.db.commit()
        self.db.refresh(db_entity)
        return db_entity

class RelationRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_relation(self, src_animal_id: int, dst_animal_id: int, relation_type: str) -> Relation:
        db_relation = Relation(
            src_animal_id=src_animal_id,
            dst_animal_id=dst_animal_id,
            relation_type=relation_type
        )
        self.db.add(db_relation)
        self.db.commit()
        self.db.refresh(db_relation)
        return db_relation