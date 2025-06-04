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


# JSON API routes

@router.post("/vineyard", response_model=schemas.Vineyard)
def create_vineyard(vineyard: schemas.VineyardCreate, session: Session = Depends(get_session)):
    db = models.Vineyard(name=vineyard.name)
    session.add(db)
    session.commit()
    session.refresh(db)
    return db

@router.get("/vineyard/{id}", response_model=schemas.Vineyard)
def read_vineyard(id: int, session: Session = Depends(get_session)):
    vineyard = session.query(models.Vineyard).get(id)
    if not vineyard:
        raise HTTPException(status_code=404, detail="Vineyard not found")
    return vineyard

@router.put("/vineyard/{id}")
def update_vineyard(id: int, name: str, address: str, session: Session = Depends(get_session)):
    vineyard = session.query(models.Vineyard).get(id)
    if not vineyard:
        raise HTTPException(status_code=404, detail="Vineyard not found")
    vineyard.name = name
    vineyard.address = address
    session.commit()
    return vineyard

@router.delete("/vineyard/{id}", status_code=204)
def delete_vineyard(id: int, session: Session = Depends(get_session)):
    vineyard = session.query(models.Vineyard).get(id)
    if not vineyard:
        raise HTTPException(status_code=404, detail="Vineyard not found")
    session.delete(vineyard)
    session.commit()


#@router.get("/vineyards", response_model=list[schemas.Vineyard])
#def list_vineyards(session: Session = Depends(get_session)):
#    return session.query(models.Vineyard).all()


# HTML routes

@router.get("/vineyards", response_class=HTMLResponse)
def vineyard_index(request: Request, session: Session = Depends(get_session)):
    vineyards = session.query(models.Vineyard).all()
    return templates.TemplateResponse(
        "vineyards.html",
        {
            "request": request,
            "vineyard": None,
            "vineyards": vineyards,
            "spray_units": [],
        }
    )

@router.get("/vineyards/{vineyard_id}", response_class=HTMLResponse)
def vineyard_form(request: Request, vineyard_id: int, session: Session = Depends(get_session)):
    vineyard = session.query(models.Vineyard).get(vineyard_id)
    if not vineyard:
        raise HTTPException(status_code=404, detail="Vineyard not found")

    vineyards = session.query(models.Vineyard).all()
    return templates.TemplateResponse(
        "vineyards.html",
        {
            "request": request,
            "vineyard": vineyard,
            "vineyards": vineyards,
            "spray_units": vineyard.spray_units,
        }
    )


@router.post("/vineyards")
def create_vineyard_html(
    name: str = Form(...),
    address: str = Form(""),
    session: Session = Depends(get_session),
):
    vineyard = models.Vineyard(name=name, address=address)
    session.add(vineyard)
    session.commit()
    return RedirectResponse(url="/vineyards", status_code=HTTP_303_SEE_OTHER)


@router.post("/vineyards/{vineyard_id}")
def update_vineyard_html(
    vineyard_id: int,
    name: str = Form(...),
    address: str = Form(""),
    session: Session = Depends(get_session),
):
    vineyard = session.query(models.Vineyard).get(vineyard_id)
    if not vineyard:
        raise HTTPException(status_code=404, detail="Vineyard not found")
    vineyard.name = name
    vineyard.address = address
    session.commit()
    return RedirectResponse(url="/vineyards", status_code=HTTP_303_SEE_OTHER)


@router.post("/vineyards/{vineyard_id}/delete")
def delete_vineyard_html(
    vineyard_id: int,
    session: Session = Depends(get_session),
):
    vineyard = session.query(models.Vineyard).get(vineyard_id)
    if vineyard:
        session.delete(vineyard)
        session.commit()
    return RedirectResponse(url="/vineyards", status_code=HTTP_303_SEE_OTHER)
