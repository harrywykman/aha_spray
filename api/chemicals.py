from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_303_SEE_OTHER
import models
import schemas
from dependencies import get_session
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# API endpoints (JSON)

@router.post("/chemical", response_model=schemas.Chemical)
def create_chemical(chemical: schemas.ChemicalCreate, session: Session = Depends(get_session)):
    db = models.Chemical(name=chemical.name, active_ingredient=chemical.active_ingredient)
    session.add(db)
    session.commit()
    session.refresh(db)
    return db

@router.get("/chemical/{id}", response_model=schemas.Chemical)
def read_chemical(id: int, session: Session = Depends(get_session)):
    chemical = session.query(models.Chemical).get(id)
    if not chemical:
        raise HTTPException(status_code=404, detail="Chemical not found")
    return chemical

@router.put("/chemical/{id}")
def update_chemical(id: int, name: str, active_ingredient: str, session: Session = Depends(get_session)):
    chemical = session.query(models.Chemical).get(id)
    if not chemical:
        raise HTTPException(status_code=404, detail="Chemical not found")
    chemical.name = name
    chemical.active_ingredient = active_ingredient
    session.commit()
    return chemical

@router.delete("/chemical/{id}", status_code=204)
def delete_chemical(id: int, session: Session = Depends(get_session)):
    chemical = session.query(models.Chemical).get(id)
    if not chemical:
        raise HTTPException(status_code=404, detail="Chemical not found")
    session.delete(chemical)
    session.commit()


@router.get("/chemicals", response_model=list[schemas.Chemical])
def list_chemicals(session: Session = Depends(get_session)):
    return session.query(models.Chemical).all()


# HTML Routes

@router.get("/chemicals", response_class=HTMLResponse)
@router.get("/chemicals/{chemical_id}", response_class=HTMLResponse)
def chemical_form(request: Request, chemical_id: int = None, session: Session = Depends(get_session)):
    chemical = session.query(models.Chemical).get(chemical_id) if chemical_id else None
    chemicals = session.query(models.Chemical).all()
    return templates.TemplateResponse("chemicals.html", {
        "request": request,
        "chemical": chemical,
        "chemicals": chemicals,
    })

@router.post("/chemicals")
def create_chemical_html(
    name: str = Form(...),
    active_ingredient: str = Form(...),
    session: Session = Depends(get_session),
):
    chemical = models.Chemical(name=name, active_ingredient=active_ingredient)
    session.add(chemical)
    session.commit()
    return RedirectResponse(url="/chemicals", status_code=HTTP_303_SEE_OTHER)

@router.post("/chemicals/{chemical_id}")
def update_chemical_html(
    chemical_id: int,
    name: str = Form(...),
    active_ingredient: str = Form(...),
    session: Session = Depends(get_session),
):
    chemical = session.query(models.Chemical).get(chemical_id)
    if not chemical:
        raise HTTPException(status_code=404, detail="Chemical not found")
    chemical.name = name
    chemical.active_ingredient = active_ingredient
    session.commit()
    return RedirectResponse(url="/chemicals", status_code=HTTP_303_SEE_OTHER)

@router.post("/chemicals/{chemical_id}/delete")
def delete_chemical_html(chemical_id: int, session: Session = Depends(get_session)):
    chemical = session.query(models.Chemical).get(chemical_id)
    if chemical:
        session.delete(chemical)
        session.commit()
    return RedirectResponse(url="/chemicals", status_code=HTTP_303_SEE_OTHER)