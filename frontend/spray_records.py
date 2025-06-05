from fastapi import APIRouter, Depends, Request, Form, HTTPException, Query
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from starlette.status import HTTP_302_FOUND

from dependencies import get_session
from models import SprayRecord, SprayUnit, SprayProgram, Vineyard

from datetime import date, datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/spray_records")
def list_spray_records(
    request: Request,
    program_id: Optional[int] = Query(None),
    complete: Optional[bool] = Query(None),
    db: Session = Depends(get_session),
):
    query = db.query(SprayRecord)
    
    if program_id is not None:
        query = query.filter(SprayRecord.spray_program_id == program_id)
    if complete is not None:
        query = query.filter(SprayRecord.complete == complete)
    
    records = query.all()
    
    return templates.TemplateResponse(
        "spray_records_list_complete_incomplete.html",
        {"request": request, "records": records}
    )

@router.get("/spray_records/{record_id}/edit")
def edit_spray_record(record_id: int, request: Request, db: Session = Depends(get_session)):
    record = db.query(SprayRecord).get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    units = db.query(SprayUnit).filter_by(vineyard_id=record.spray_unit.vineyard_id).all()
    programs = db.query(SprayProgram).all()

    return templates.TemplateResponse("spray_records_edit.html", {
        "request": request,
        "record": record,
        "units": units,
        "programs": programs,
        "vineyard_id": record.spray_unit.vineyard_id,
    })


@router.post("/spray_records/{record_id}/edit")
def update_spray_record(
    record_id: int,
    date: str = Form(...),
    el: int = Form(...),
    operator: str = Form(...),
    wind_speed: int = Form(...),
    wind_direction: str = Form(...),
    temp: int = Form(...),
    relative_humidity: int = Form(...),
    spray_unit_id: int = Form(...),
    spray_program_id: int = Form(...),
    complete: bool = Form(False),
    db: Session = Depends(get_session)
):
    record = db.query(SprayRecord).get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    # Parse the date string into a datetime.date object
    try:
        record.date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Expected YYYY-MM-DD.")

    record.el = el
    record.operator = operator
    record.wind_speed = wind_speed
    record.wind_direction = wind_direction
    record.temp = temp
    record.relative_humidity = relative_humidity
    record.spray_unit_id = spray_unit_id
    record.spray_program_id = spray_program_id
    record.complete = complete

    db.commit()

    return RedirectResponse(url=f"/vineyards/{record.spray_unit.vineyard_id}", status_code=HTTP_302_FOUND)


@router.get("/spray_records/{record_id}/delete")
def delete_spray_record(record_id: int, db: Session = Depends(get_session)):
    record = db.query(SprayRecord).get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    vineyard_id = record.spray_unit.vineyard_id

    db.delete(record)
    db.commit()
    return RedirectResponse(url=f"/vineyards/{vineyard_id}", status_code=HTTP_302_FOUND)

# List Spray Records for a Vineyard
@router.get("/vineyards/{vineyard_id}/spray_records")
def list_spray_records(vineyard_id: int, request: Request, db: Session = Depends(get_session)):
    vineyard = db.query(Vineyard).get(vineyard_id)
    if not vineyard:
        raise HTTPException(status_code=404, detail="Vineyard not found")
    spray_records = (
        db.query(SprayRecord)
        .join(SprayUnit)
        .filter(SprayUnit.vineyard_id == vineyard_id)
        .all()
    )
    return templates.TemplateResponse("list_spray_records.html", {
        "request": request,
        "vineyard": vineyard,
        "spray_records": spray_records
    })

# New Spray Record form
@router.get("/vineyards/{vineyard_id}/spray_records/new")
def new_spray_record_form(vineyard_id: int, request: Request, db: Session = Depends(get_session)):
    units = db.query(SprayUnit).filter_by(vineyard_id=vineyard_id).all()
    programs = db.query(SprayProgram).all()
    return templates.TemplateResponse("spray_records_form.html", {
        "request": request,
        "vineyard_id": vineyard_id,
        "units": units,
        "programs": programs,
        "record": None
    })

# Create spray record
@router.post("/vineyards/{vineyard_id}/spray_records")
def create_spray_record(
    vineyard_id: int,
    date: date = Form(...),
    el: int = Form(...),
    operator: str = Form(...),
    wind_speed: int = Form(...),
    wind_direction: str = Form(...),
    temp: int = Form(...),
    relative_humidity: int = Form(...),
    spray_unit_id: int = Form(...),
    spray_program_id: int = Form(...),
    complete: bool = Form(False),
    db: Session = Depends(get_session)
):
    record = SprayRecord(
        date=date,
        el=el,
        operator=operator,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        temp=temp,
        relative_humidity=relative_humidity,
        spray_unit_id=spray_unit_id,
        spray_program_id=spray_program_id,
        complete=complete
    )
    db.add(record)
    db.commit()
    return RedirectResponse(f"/vineyards/{vineyard_id}/spray_records", status_code=302)
