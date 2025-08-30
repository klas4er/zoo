#!/usr/bin/env python3

"""
Script to seed the database with initial data for animals, foods, and locations.
"""

from backend.database import SessionLocal
from backend.models import Animal

def seed_data():
    """Seed database with initial data"""
    db = SessionLocal()
    
    # Check if animals already exist
    existing_animals = db.query(Animal).count()
    if existing_animals > 0:
        print("Database already seeded. Skipping.")
        db.close()
        return
    
    # Create initial animals
    animals = [
        Animal(species="giraffe", name="Жужа", tags={"gender": "female", "age": 8}),
        Animal(species="elephant", name="Dima", tags={"gender": "male", "age": 12}),
        Animal(species="bear", name="Sonya", tags={"gender": "female", "age": 5}),
        Animal(species="lion", name="Rita", tags={"gender": "female", "age": 5}),
        Animal(species="tiger", name="Amur", tags={"gender": "male", "age": 7}),
    ]
    
    # Add animals to database
    for animal in animals:
        db.add(animal)
    
    # Commit changes
    db.commit()
    db.close()
    
    print("Database seeded successfully with initial animals.")

if __name__ == "__main__":
    seed_data()