from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
import models
import schemas


# Create db
Base.metadata.create_all(engine)

# Initialise Fast API app
app = FastAPI()

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/")
async def root():
    return {"message": "Spray Records"}

# Vineyards

@app.post("/vineyard", response_model=schemas.Vineyard, status_code=status.HTTP_201_CREATED)
def create_vineyard(vineyard: schemas.VineyardCreate, session: Session = Depends(get_session)):

    session = SessionLocal()

    db = models.Vineyard(name = vineyard.name)
    session.add(db)
    session.commit()
    session.refresh(db)

    return db

@app.get("/vineyard/{id}", response_model=schemas.Vineyard)
def read_vineyard(id: int, session: Session = Depends(get_session)):

    vineyard = session.query(models.Vineyard).get(id)

    if not vineyard:
        raise HTTPException(status_code=404, detail=f"Vineyard with id {id} not found")

    return vineyard

# Spray Records

@app.post("/spray_record", response_model=schemas.SprayRecord, status_code=status.HTTP_201_CREATED)
def create_spray_record(spray_record: schemas.SprayRecordCreate, session: Session = Depends(get_session)):

    session = SessionLocal()

    db = models.SprayRecord(date = spray_record.date,
                     el = spray_record.el,
                     operator = spray_record.operator,
                     wind_speed = spray_record.wind_speed,
                     wind_direction = spray_record.wind_direction,
                     temp = spray_record.temp,
                     relative_humidity = spray_record.relative_humidity
                     )
    
    session.add(db)
    session.commit()
    session.refresh(db)

    return db

@app.get("/spray_record/{id}", response_model=schemas.SprayRecord)
def read_spray_record(id: int, session: Session = Depends(get_session)):

    spray_record = session.query(models.SprayRecord).get(id)

    if not spray_record:
        raise HTTPException(status_code=404, detail=f"Spray record item with id {id} not found")

    return spray_record

@app.put("/spray_record/{id}")
def update_spray_record(id: int, 
                        #date: date,
                        el: int,
                        #operator: str,
                        #wind_speed: int,
                        #wind_direction: str,
                        #temp: int,
                        #relative_humidity: int,
                        session: Session = Depends(get_session)
                        ):

    spray_record = session.query(models.SprayRecord).get(id)

    if spray_record:
        #if new_date: 
        #    spray_record.date = new_date
        if el:
            spray_record.el = el
        #spray_record.operator = operator
        #spray_record.wind_speed = wind_speed
        #spray_record.wind_direction = wind_direction
        #spray_record.temp = temp
        #spray_record.relative_humidity = relative_humidity
        session.commit()

    if not spray_record:
        raise HTTPException(status_code=404, detail=f"Spray record item with id {id} not found")

    return spray_record

@app.delete("/spray_record/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_spray_record(id: int, session: Session = Depends(get_session)):

    spray_record = session.query(models.SprayRecord).get(id)

    if spray_record:
        session.delete(spray_record)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Spray record item with id {id} not found")

    return None

@app.get("/spray_record", response_model = List[schemas.SprayRecord])
def read_spray_record_list(session: Session = Depends(get_session)):

    spray_record_list = session.query(models.SprayRecord).all()

    return spray_record_list