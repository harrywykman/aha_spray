# api/spray_records.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from dependencies import get_session

router = APIRouter(prefix="/api/spray_records", tags=["Spray Records"])


# These are all api endpoints, left here as model for html routes

@router.post("/", response_model=schemas.SprayRecord, status_code=status.HTTP_201_CREATED)
def create_spray_record(spray_record: schemas.SprayRecordCreate, session: Session = Depends(get_session)):
    db = models.SprayRecord(
        date=spray_record.date,
        el=spray_record.el,
        operator=spray_record.operator,
        wind_speed=spray_record.wind_speed,
        wind_direction=spray_record.wind_direction,
        temp=spray_record.temp,
        relative_humidity=spray_record.relative_humidity
    )
    session.add(db)
    session.commit()
    session.refresh(db)
    return db

@router.get("/", response_model=List[schemas.SprayRecord])
def list_spray_records(session: Session = Depends(get_session)):
    return session.query(models.SprayRecord).all()

@router.get("/{id}", response_model=schemas.SprayRecord)
def get_spray_record(id: int, session: Session = Depends(get_session)):
    spray_record = session.query(models.SprayRecord).get(id)
    if not spray_record:
        raise HTTPException(status_code=404, detail="Spray record not found")
    return spray_record

@router.put("/{id}", response_model=schemas.SprayRecord)
def update_spray_record(id: int, spray_data: schemas.SprayRecordCreate, session: Session = Depends(get_session)):
    spray_record = session.query(models.SprayRecord).get(id)
    if not spray_record:
        raise HTTPException(status_code=404, detail="Spray record not found")

    for key, value in spray_data.dict().items():
        setattr(spray_record, key, value)
    session.commit()
    return spray_record

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_spray_record(id: int, session: Session = Depends(get_session)):
    spray_record = session.query(models.SprayRecord).get(id)
    if not spray_record:
        raise HTTPException(status_code=404, detail="Spray record not found")

    session.delete(spray_record)
    session.commit()
    return None