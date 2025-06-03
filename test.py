from nicegui import ui
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import models
import schemas
from database import Base, engine, SessionLocal

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

# --- UI state ---
editing_id = None

# --- Form Fields ---
name_input = ui.input('Name')
ingredient_input = ui.input('Active Ingredient')
submit_button = ui.button('Add Chemical', on_click=lambda: add_or_update())

ui.separator()

# --- Chemical List Table ---
table = ui.table(columns=[
    {'name': 'id', 'label': 'ID', 'field': 'id'},
    {'name': 'name', 'label': 'Name', 'field': 'name'},
    {'name': 'active_ingredient', 'label': 'Active Ingredient', 'field': 'active_ingredient'},
    {'name': 'actions', 'label': 'Actions', 'field': 'actions'},
], rows=[], row_key='id').classes('w-full')

# --- CRUD Logic ---

def load_chemicals():
    session = SessionLocal()
    chemicals = session.query(models.Chemical).all()
    table.rows = [{
        'id': c.id,
        'name': c.name,
        'active_ingredient': c.active_ingredient,
        'actions': f'<button onclick="window.location.href=\'/edit/{c.id}\'">Edit</button> '
                   f'<button onclick="window.location.href=\'/delete/{c.id}\'">Delete</button>',
    } for c in chemicals]
    session.close()

def add_or_update():
    global editing_id
    try:
        data = schemas.Chemical(name=name_input.value, active_ingredient=ingredient_input.value)
    except Exception as e:
        ui.notify(f'Validation Error: {e}')
        return

    session = SessionLocal()
    if editing_id:
        chemical = session.query(models.Chemical).get(editing_id)
        if chemical:
            chemical.name = data.name
            chemical.active_ingredient = data.active_ingredient
            ui.notify('Chemical updated')
    else:
        chemical = models.Chemical(name=data.name, active_ingredient=data.active_ingredient)
        session.add(chemical)
        ui.notify('Chemical added')

    session.commit()
    session.close()
    clear_form()
    load_chemicals()

def edit_chemical(chemical_id: int):
    global editing_id
    session = SessionLocal()
    chemical = session.query(models.Chemical).get(chemical_id)
    if chemical:
        editing_id = chemical.id
        name_input.value = chemical.name
        ingredient_input.value = chemical.active_ingredient
        submit_button.text = 'Update Chemical'
    session.close()

def delete_chemical(chemical_id: int):
    session = SessionLocal()
    chemical = session.query(models.Chemical).get(chemical_id)
    if chemical:
        session.delete(chemical)
        session.commit()
        ui.notify('Chemical deleted')
    session.close()
    load_chemicals()

def clear_form():
    global editing_id
    name_input.value = ''
    ingredient_input.value = ''
    editing_id = None
    submit_button.text = 'Add Chemical'

# --- Load initial data ---
load_chemicals()

@ui.page('/edit/{chemical_id}')
def edit_page(chemical_id: int):
    edit_chemical(chemical_id)

@ui.page('/delete/{chemical_id}')
def delete_page(chemical_id: int):
    delete_chemical(chemical_id)

ui.run()