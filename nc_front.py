from nicegui import ui
from pydantic import BaseModel

from sqlalchemy.orm import Session
from fastapi import Depends

from database import SessionLocal
import models
import schemas

import logging

from niceguicrud import NiceCRUD

#log = logging.getLogger("niceguicrud")
#log.setLevel(logging.DEBUG)
#console_handler = logging.StreamHandler()
#console_handler.setFormatter(logging.Formatter("%(levelname)s - %(name)s - %(message)s"))
#log.addHandler(console_handler)

# Helper function to get DB session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# Get actual session instance, not a dependency wrapper
session: Session = next(get_session())

# Retrieve data
chemical_list = session.query(models.Chemical).all()

# Convert SQLAlchemy objects to list of dicts / Pydantic models if needed
chemical_data = [schemas.Chemical.model_validate(chem) for chem in chemical_list]

crud_app = NiceCRUD(
    basemodels=chemical_data,
    #db_model=models.Chemical,
    #session=session,
    id_field="id",
    heading="Chemical Management",
)

class ChemicalCRUD(NiceCRUD):
    async def update(self, chemical: schemas.Chemical, session):
        ui.notify(f"Custom database update: {chemical.id} - {chemical.name}")

        db_chem = session.query(models.Chemical).filter(models.Chemical.id == chemical.id).first()
        if db_chem:
            db_chem.name = chemical.name
            db_chem.active_ingredient = chemical.active_ingredient
            session.commit()
            session.refresh(db_chem)
            print(f"Updated in DB: {db_chem.id}, {db_chem.name}")
        else:
            print(f"Chemical ID {chemical.id} not found.")

        await super().update(chemical)

    async def create(self, chemical: schemas.ChemicalCreate):
        ui.notify(f"Custom database create: {chemical.name}")
        session = next(get_session())

        db_chem = models.Chemical(
            name=chemical.name,
            active_ingredient=chemical.active_ingredient,
        )
        session.add(db_chem)
        session.commit()
        session.refresh(db_chem)

        await super().create(chemical)

    async def delete(self, chemical: schemas.Chemical):
        ui.notify(f"Custom database delete: {chemical.id}")
        session = next(get_session())

        db_chem = session.query(models.Chemical).filter(models.Chemical.id == chemical.id).first()
        if db_chem:
            session.delete(db_chem)
            session.commit()
            print(f"Updated in DB: {db_chem.id}, {db_chem.name}")
        else:
            print(f"Chemical ID {chemical.id} not found.")

        await super().delete(chemical)

    """async def select_options(self, field_name: str, schemas.Chemical) -> dict:
        if field_name == "color":
            # this can be taken from the database, too
            if unicorn.sparkle_level > 10:
                return dict(red="Red", pink="Pink", rainbow="Rainbow")
            else:
                return dict(red="Red", pink="Pink")
        else:
            return await super().select_options(field_name, unicorn)
    """



ui.run()


""" from nicegui import ui
from pydantic import BaseModel, Field

from fastapi import FastAPI, Request, Depends

from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal

import schemas
import models

from niceguicrud import NiceCRUD

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

session: Session = Depends(get_session)

chemical_list = Session.query(models.Chemical).all()


crud_app = NiceCRUD(basemodels=chemical_list, 
                    id_field="id", 
                    heading="User Management")

ui.run() """