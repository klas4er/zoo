from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Animal(Base):
    __tablename__ = "animals"
    
    id = Column(Integer, primary_key=True, index=True)
    species = Column(String, index=True)
    name = Column(String)
    tags = Column(JSON)
    
    observations = relationship("Observation", back_populates="animal")

class Observation(Base):
    __tablename__ = "observations"
    
    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id"), index=True)
    watcher_id = Column(Integer, index=True)
    ts = Column(DateTime, default=datetime.utcnow, index=True)
    raw_text = Column(Text)
    confidence = Column(Float)
    
    animal = relationship("Animal", back_populates="observations")
    entities = relationship("ObservationEntity", back_populates="observation")

class ObservationEntity(Base):
    __tablename__ = "observation_entities"
    
    id = Column(Integer, primary_key=True, index=True)
    observation_id = Column(Integer, ForeignKey("observations.id"), index=True)
    type = Column(String, index=True)
    payload_json = Column(JSON)
    
    observation = relationship("Observation", back_populates="entities")

class Relation(Base):
    __tablename__ = "relations"
    
    id = Column(Integer, primary_key=True, index=True)
    src_animal_id = Column(Integer, ForeignKey("animals.id"), index=True)
    dst_animal_id = Column(Integer, ForeignKey("animals.id"), index=True)
    relation_type = Column(String)
    ts = Column(DateTime, default=datetime.utcnow)
    
    src_animal = relationship("Animal", foreign_keys=[src_animal_id])
    dst_animal = relationship("Animal", foreign_keys=[dst_animal_id])