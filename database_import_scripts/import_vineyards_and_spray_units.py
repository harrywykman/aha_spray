import csv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# --- SQLAlchemy Models ---
Base = declarative_base()

class Vineyard(Base):
    __tablename__ = 'vineyards'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)

    spray_units = relationship("SprayUnit", back_populates="vineyard", cascade="all, delete-orphan")

class SprayUnit(Base):
    __tablename__ = 'spray_units'

    id = Column(Integer, primary_key=True)
    vineyard_id = Column(Integer, ForeignKey('vineyards.id'), nullable=False)
    name = Column(String, nullable=False)

    vineyard = relationship("Vineyard", back_populates="spray_units")

# --- Setup ---
engine = create_engine('sqlite:///../spray_records.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# --- Helpers ---
def normalize_name(name: str) -> str:
    return name.strip().title()

def get_or_create_vineyard(name, address):
    normalized_name = normalize_name(name)
    vineyard = session.query(Vineyard).filter(func.lower(Vineyard.name) == normalized_name.lower()).first()
    if not vineyard:
        vineyard = Vineyard(name=normalized_name, address=address.strip() if address else None)
        session.add(vineyard)
        session.flush()
    return vineyard

def add_spray_units(vineyard, unit_names):
    existing_units = {unit.name.lower() for unit in vineyard.spray_units}
    new_count = 0
    for unit_name in unit_names:
        name = unit_name.strip()
        if name and name.upper() != "ALL" and name.lower() not in existing_units:
            session.add(SprayUnit(name=name, vineyard=vineyard))
            new_count += 1
    return new_count

# --- Main Import Logic ---
def import_vineyards_and_spray_units(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        vineyard_count = 0
        spray_unit_count = 0

        for row in reader:
            raw_name = row['NAME']
            raw_address = row['ADDRESS']

            # Collect all spray unit fields by name prefix
            spray_units = [value for key, value in row.items() if key.startswith('SPRAY UNIT') and value and value.strip()]

            # Get or create vineyard
            vineyard = get_or_create_vineyard(raw_name, raw_address)
            prev_unit_total = len(vineyard.spray_units)

            # Add Spray Units
            added_units = add_spray_units(vineyard, spray_units)
            spray_unit_count += added_units

            if prev_unit_total == 0 and added_units > 0:
                vineyard_count += 1

        session.commit()
        print(f"Import complete.")
        print(f"New or updated vineyards: {vineyard_count}")
        print(f"Spray units added: {spray_unit_count}")

# --- Run ---
if __name__ == "__main__":
    import_vineyards_and_spray_units("./data/vineyard_addresses_spray_units.csv")  # Update path if needed




