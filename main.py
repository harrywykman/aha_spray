from fastapi import FastAPI, status
from database import Base, engine, SprayRecord
from pydantic import BaseModel
from datetime import date
from sqlalchemy.orm import Session

# Create SprayRecordRequest Base Model
class SprayRecordRequest(BaseModel):
    date: date
    el: int
    operator: str
    wind_speed: int
    wind_direction: str
    temp: int
    relative_humidity: int

# Create db
Base.metadata.create_all(engine)

# Initialise Fast API app
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Spray Records"}

@app.post("/spray_record", status_code=status.HTTP_201_CREATED)
def create_spray_record(spray_record: SprayRecordRequest):

    session = Session(bind=engine, expire_on_commit=False)

    db = SprayRecord(date = spray_record.date,
                     el = spray_record.el,
                     operator = spray_record.operator,
                     wind_speed = spray_record.wind_speed,
                     wind_direction = spray_record.wind_direction,
                     temp = spray_record.temp,
                     relative_humidity = spray_record.relative_humidity
                     )
    
    session.add(db)
    session.commit()

    id = db.id

    session.close()

    return f"Created spray record with id {id}"

@app.get("/spray_record/{id}")
def read_spray_record(id: int):
    return "Read Spray Record Item with ID {id}"

@app.put("/spray_record/{id}")
def update_spray_record(id: int):
    return "Update Spray Record Item with ID {id}"

@app.delete("/spray_record/{id}")
def delete_spray_record(id: int):
    return "Delete Spray Record Item with ID {id}"

@app.get("/spray_record")
def read_spray_record():
    return "Read Spray Record List"