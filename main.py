from fastapi import FastAPI, status, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from slugify import slugify
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

# Front End

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def list_vineyards_html(request: Request, session: Session = Depends(get_session)):

    vineyard_list = session.query(models.Vineyard).all()

    return templates.TemplateResponse(
        request=request, name="vineyards.html", context={"vineyards": vineyard_list}
    )

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