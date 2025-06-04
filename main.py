from fastapi import FastAPI, status, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from slugify import slugify
from typing import List
import models
import schemas
import frontend
from starlette.status import HTTP_303_SEE_OTHER

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

# Front End

## jinja only

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# HTML view to list and edit chemicals
@app.get("/chemicals", response_class=HTMLResponse)
@app.get("/chemicals/{chemical_id}", response_class=HTMLResponse)
def chemical_form(
    request: Request,
    chemical_id: int = None,
    session: Session = Depends(get_session)
):
    chemical = session.query(models.Chemical).get(chemical_id) if chemical_id else None
    chemicals = session.query(models.Chemical).all()
    return templates.TemplateResponse(
        "chemicals.html",
        {
            "request": request,
            "chemical": chemical,
            "chemicals": chemicals,
        }
    )

# Create new chemical via HTML form
@app.post("/chemicals")
def create_chemical_html(
    request: Request,
    name: str = Form(...),
    active_ingredient: str = Form(...),
    session: Session = Depends(get_session),
):
    chemical = models.Chemical(name=name, active_ingredient=active_ingredient)
    session.add(chemical)
    session.commit()
    return RedirectResponse(url="/chemicals", status_code=HTTP_303_SEE_OTHER)

# Update existing chemical via HTML form
@app.post("/chemicals/{chemical_id}")
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

# Delete chemical via HTML form
@app.post("/chemicals/{chemical_id}/delete")
def delete_chemical_html(
    chemical_id: int,
    session: Session = Depends(get_session),
):
    chemical = session.query(models.Chemical).get(chemical_id)
    if chemical:
        session.delete(chemical)
        session.commit()
    return RedirectResponse(url="/chemicals", status_code=HTTP_303_SEE_OTHER)

@app.get("/vineyards", response_class=HTMLResponse)
def vineyard_index(
    request: Request,
    session: Session = Depends(get_session),
    ):
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

# HTML view to list and edit vineyards
@app.get("/vineyards", response_class=HTMLResponse)
@app.get("/vineyards/{vineyard_id}", response_class=HTMLResponse)
def vineyard_form(
    request: Request,
    vineyard_id: int,
    session: Session = Depends(get_session),
):
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
"""
@app.get("/vineyards/{vineyard_id}", response_class=HTMLResponse)
def vineyard_form(
    request: Request,
    vineyard_id: int = None,
    session: Session = Depends(get_session),
):
    vineyard = session.query(models.Vineyard).get(vineyard_id) if vineyard_id else None
    vineyards = session.query(models.Vineyard).all()
    return templates.TemplateResponse(
        "vineyards.html",
        {
            "request": request,
            "vineyard": vineyard,
            "vineyards": vineyards,
        }
    )
"""


# Create new vineyard via HTML form
@app.post("/vineyards")
def create_vineyard_html(
    name: str = Form(...),
    address: str = Form(""),
    session: Session = Depends(get_session),
):
    vineyard = models.Vineyard(name=name, address=address)
    session.add(vineyard)
    session.commit()
    return RedirectResponse(url="/vineyards", status_code=HTTP_303_SEE_OTHER)

# Update existing vineyard via HTML form
@app.post("/vineyards/{vineyard_id}")
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
    

# Delete vineyard via HTML form
@app.post("/vineyards/{vineyard_id}/delete")
def delete_vineyard_html(
    vineyard_id: int,
    session: Session = Depends(get_session),
):
    vineyard = session.query(models.Vineyard).get(vineyard_id)
    if vineyard:
        session.delete(vineyard)
        session.commit()
    return RedirectResponse(url="/vineyards", status_code=HTTP_303_SEE_OTHER)


@app.get("/", response_class=HTMLResponse)
async def list_vineyards_html(request: Request, session: Session = Depends(get_session)):

    vineyard_list = session.query(models.Vineyard).all()

    return templates.TemplateResponse(
        request=request, name="vineyards.html", context={"vineyards": vineyard_list}
    )

# SPRAY UNITS

@app.post("/vineyards/{vineyard_id}/spray_units")
def add_spray_unit(
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

@app.get("/spray_units/{unit_id}/edit", response_class=HTMLResponse)
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


@app.post("/spray_units/{unit_id}/edit")
def update_spray_unit(
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

@app.post("/spray_units/{unit_id}/delete")
def delete_spray_unit(unit_id: int, session: Session = Depends(get_session)):
    unit = session.query(models.SprayUnit).get(unit_id)
    vineyard_id = unit.vineyard_id
    if unit:
        session.delete(unit)
        session.commit()
    return RedirectResponse(url=f"/vineyards/{vineyard_id}", status_code=303)


# Chemicals

@app.post("/chemical", response_model=schemas.Chemical, status_code=status.HTTP_201_CREATED)
def create_chemical(chemical: schemas.ChemicalCreate, session: Session = Depends(get_session)):

    session = SessionLocal()

    db = models.Chemical(name = chemical.name,
                         active_ingredient = chemical.active_ingredient,
                         )
    session.add(db)
    session.commit()
    session.refresh(db)

    return db

@app.get("/chemical/{id}", response_model=schemas.Chemical)
def read_chemical(id: int, session: Session = Depends(get_session)):

    chemical = session.query(models.Chemical).get(id)

    if not chemical:
        raise HTTPException(status_code=404, detail=f"Chemical with id {id} not found")

    return chemical

@app.put("/chemical/{id}")
def update_chemical(id: int, 
                        name: str,
                        active_ingredient: str,
                        session: Session = Depends(get_session)
                        ):

    chemical = session.query(models.Chemical).get(id)

    if chemical:
        if name: 
            chemical.name = name        
        if active_ingredient:
            chemical.active_ingredient = active_ingredient
        session.commit()

    if not chemical:
        raise HTTPException(status_code=404, detail=f"Chemical with id {id} not found")

    return chemical

@app.delete("/chemical/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chemical(id: int, session: Session = Depends(get_session)):

    chemical = session.query(models.Chemical).get(id)

    if chemical:
        session.delete(chemical)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Chemical with id {id} not found")

    return None

@app.get("/chemicals", response_model = List[schemas.Chemical])
def read_chemical_list(session: Session = Depends(get_session)):

    chemical_list = session.query(models.Chemical).all()

    return chemical_list


# Vineyards

@app.post("/vineyard", response_model=schemas.Vineyard, status_code=status.HTTP_201_CREATED)
def create_vineyard(vineyard: schemas.VineyardCreate, session: Session = Depends(get_session)):

    session = SessionLocal()

    db = models.Vineyard(name = vineyard.name,
                         )
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

@app.put("/vineyard/{id}")
def update_vineyard(id: int, 
                        name: str,
                        address: str,
                        session: Session = Depends(get_session)
                        ):

    vineyard = session.query(models.Vineyard).get(id)

    if vineyard:
        if name: 
            vineyard.name = name        
        if address:
            vineyard.address = address
        session.commit()

    if not vineyard:
        raise HTTPException(status_code=404, detail=f"Vineyard with id {id} not found")

    return vineyard

@app.delete("/vineyard/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vineyard(id: int, session: Session = Depends(get_session)):

    vineyard = session.query(models.Vineyard).get(id)

    if vineyard:
        session.delete(vineyard)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Vineyard with id {id} not found")

    return None

@app.get("/vineyards", response_model = List[schemas.Vineyard])
def read_vineyard_list(session: Session = Depends(get_session)):

    vineyard_list = session.query(models.Vineyard).all()

    return vineyard_list

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

@app.get("/spray_records", response_model = List[schemas.SprayRecord])
def read_spray_record_list(session: Session = Depends(get_session)):

    spray_record_list = session.query(models.SprayRecord).all()

    return spray_record_list