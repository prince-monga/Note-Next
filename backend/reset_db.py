#!/usr/bin/env python3
"""
Script to reset the database with new schema
"""
import os
from database import Base, engine

def reset_database():
    # Remove existing database file
    db_file = "notes.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        print("Removed existing database")
    
    # Create new database with updated schema
    Base.metadata.create_all(bind=engine)
    print("Created new database with updated schema")

if __name__ == "__main__":
    reset_database()