from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_303_SEE_OTHER
from fastapi.templating import Jinja2Templates

import models
import schemas
from dependencies import get_session

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# API Routes

@router.post("/spray_unit", response_model=schemas.SprayUnit, status_code=201)
def create_spray_unit(spray_unit: schemas.SprayUnitCreate, session: Session = Depends(get_session)):
    db = models.SprayUnit(**spray_unit.dict())
    session.add(db)
    session.commit()
    session.refresh(db)
    return db

@router.get("/spray_unit/{id}", response_model=schemas.SprayUnit)
def read_spray_unit(id: int, session: Session = Depends(get_session)):
    unit = session.query(models.SprayUnit).get(id)
    if not unit:
        raise HTTPException(status_code=404, detail="Spray unit not found")
    return unit

@router.put("/spray_unit/{id}")
def update_spray_unit_api(
    id: int,
    name: str,
    session: Session = Depends(get_session)
):
    unit = session.query(models.SprayUnit).get(id)
    if not unit:
        raise HTTPException(status_code=404, detail="Spray unit not found")

    unit.name = name
    session.commit()
    return unit

@router.delete("/spray_unit/{id}", status_code=204)
def delete_spray_unit_api(id: int, session: Session = Depends(get_session)):
    unit = session.query(models.SprayUnit).get(id)
    if not unit:
        raise HTTPException(status_code=404, detail="Spray unit not found")
    session.delete(unit)
    session.commit()

@router.get("/spray_units", response_model=list[schemas.SprayUnit])
def list_spray_units(session: Session = Depends(get_session)):
    return session.query(models.SprayUnit).all()

# HTML Form Routes

@router.post("/vineyards/{vineyard_id}/spray_units")
def add_spray_unit_html(
    vineyard_id: int,
    name: str = Form(...),
    session: Session = Depends(get_session),
):
    vineyard = session.query(models.Vineyard).get(vineyard_id)
    if not vineyard:
        raise HTTPException(status_code=404, detail="Vineyard not found")

    unit = models.SprayUnit(name=name, vineyard_id=vineyard_id)
    session.add(unit)
    session.commit()

    return RedirectResponse(url=f"/vineyards/{vineyard_id}", status_code=HTTP_303_SEE_OTHER)

@router.get("/spray_units/{unit_id}/edit", response_class=HTMLResponse)
def edit_spray_unit_form(
    unit_id: int,
    request: Request,
    session: Session = Depends(get_session),
):
    unit = session.query(models.SprayUnit).get(unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Spray unit not found")

    return templates.TemplateResponse("edit_spray_unit.html", {
        "request": request,
        "unit": unit
    })

@router.post("/spray_units/{unit_id}/edit")
def update_spray_unit_html(
    unit_id: int,
    name: str = Form(...),
    session: Session = Depends(get_session),
):
    unit = session.query(models.SprayUnit).get(unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Spray unit not found")

    unit.name = name
    session.commit()

    return RedirectResponse(url=f"/vineyards/{unit.vineyard_id}", status_code=HTTP_303_SEE_OTHER)

@router.post("/spray_units/{unit_id}/delete")
def delete_spray_unit_html(unit_id: int, session: Session = Depends(get_session)):
    unit = session.query(models.SprayUnit).get(unit_id)
    vineyard_id = unit.vineyard_id if unit else None

    if unit:
        session.delete(unit)
        session.commit()

    return RedirectResponse(url=f"/vineyards/{vineyard_id}", status_code=HTTP_303_SEE_OTHER)