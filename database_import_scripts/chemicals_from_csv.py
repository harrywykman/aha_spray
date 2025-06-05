import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Chemical, Base  # Assumes models.py contains your Chemical model
import os
from dependencies import get_session

from database import engine  # assuming you have an engine in database.py

DATABASE_URL = "sqlite:///../spray_records.db"  # <-- Change this if needed

# Set up the database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def load_chemicals_from_csv(csv_file_path):
    session = SessionLocal()
    added_count = 0
    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['name'].strip()
                active_ingredient = row['active_ingredient'].strip()

                # Check if the chemical already exists
                existing = session.query(Chemical).filter_by(
                    name=name, active_ingredient=active_ingredient
                ).first()

                if not existing:
                    new_chemical = Chemical(
                        name=name,
                        active_ingredient=active_ingredient
                    )
                    session.add(new_chemical)
                    added_count += 1

            session.commit()
            print(f"✅ Added {added_count} new chemicals.")
    except Exception as e:
        session.rollback()
        print("❌ Error:", e)
    finally:
        session.close()

if __name__ == "__main__":
    CSV_PATH = "./data/chemicals.csv"  # Change this if your file is named differently
    if not os.path.exists(CSV_PATH):
        print(f"CSV file not found: {CSV_PATH}")
    else:
        load_chemicals_from_csv(CSV_PATH)
