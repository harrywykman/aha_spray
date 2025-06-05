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

from api import chemicals, vineyards, spray_units, spray_records
from frontend import chemicals, vineyards, spray_units, spray_records, spray_programs

# Initialise Fast API app
app = FastAPI()

app.include_router(chemicals.router, prefix="/api")
app.include_router(vineyards.router, prefix="/api")
app.include_router(spray_units.router, prefix="/api")
app.include_router(spray_records.router, prefix="/api")

app.include_router(chemicals.router)
app.include_router(vineyards.router)
app.include_router(spray_units.router)
app.include_router(spray_records.router)
app.include_router(spray_programs.router)


# Create db
Base.metadata.create_all(engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
