import csv
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# --- SQLAlchemy setup ---
Base = declarative_base()

class Vineyard(Base):
    __tablename__ = 'vineyards'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)

# --- Database Initialization ---
engine = create_engine('sqlite:///../spray_records.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# --- Helper: Clean and regularize name ---
def normalize_name(name: str) -> str:
    return name.strip().title()

# --- Load from CSV with deduplication ---
def load_vineyards_from_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        added = 0
        skipped = 0

        for row in reader:
            raw_name = row['NAME'].strip()
            name = normalize_name(raw_name)
            address = row['ADDRESS'].strip() if row['ADDRESS'] else None

            # Check for duplicates by case-insensitive name
            existing = session.query(Vineyard).filter(func.lower(Vineyard.name) == name.lower()).first()
            if existing:
                print(f"Skipped duplicate: {name}")
                skipped += 1
                continue

            vineyard = Vineyard(name=name, address=address)
            session.add(vineyard)
            added += 1

        session.commit()
        print(f"Done. Added {added} vineyard(s), skipped {skipped} duplicate(s).")

# --- Run ---
if __name__ == "__main__":
    load_vineyards_from_csv('./data/vineyard_addresses.csv')  # Adjust filename/path if needed
