from fastapi import FastAPI, Request, Depends

from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal

from nicegui import app, ui

import models

# Initialise Fast API app
fastapi_app = FastAPI()

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init(fastapi_app):
    @ui.page('/')
    def show(request: Request, session: Session = Depends(get_session)):
        ui.label('Hello, FastAPI!')

        vineyard_list = session.query(models.Vineyard).all()

        ui.label(vineyard_list[1].name)

        for vineyard in vineyard_list:
            ui.label(f"{ vineyard.name }")
            print(f"{ vineyard.name }")
            ui.label('test')

        # NOTE dark mode will be persistent for each user across tabs and server restarts
        ui.dark_mode().bind_value(app.storage.user, 'dark_mode')
        ui.checkbox('dark mode').bind_value(app.storage.user, 'dark_mode')

    ui.run_with(
        fastapi_app,
        mount_path='/gui',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret='pick your private secret here',  # NOTE setting a secret is optional but allows for persistent storage per user
    )