from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.status import HTTP_303_SEE_OTHER
from dependencies import get_session
import models
import schemas

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/spray_programs/{program_id}/add_to_all_units")
async def add_program_to_all_units(program_id: int, db: Session = Depends(get_session)):
    program = db.query(models.SprayProgram).filter(models.SprayProgram.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="SprayProgram not found")

    # Query all spray units
    all_units = db.query(models.SprayUnit).all()

    # Logic here to associate `program` with all `spray_units`
    # For example, set program.spray_unit_id or create SprayRecords as needed

    for unit in all_units:
        # Example: create SprayRecord linking this program and spray unit
        new_record = models.SprayRecord(
            date=program.date,
            spray_unit_id=unit.id,
            spray_program_id=program.id,
            complete=False,
            # Add any other defaults as needed
        )
        db.add(new_record)

    db.commit()

    return {"message": f"Program {program.number} added to all spray units."}



@router.get("/spray_programs", response_class=HTMLResponse)
def list_spray_programs(request: Request, session: Session = Depends(get_session)):
    programs = session.query(models.SprayProgram).all()
    return templates.TemplateResponse("spray_programs.html", {
        "request": request,
        "programs": programs
    })

@router.get("/spray_programs/new", response_class=HTMLResponse)
def new_spray_program(request: Request, session: Session = Depends(get_session)):
    chemicals = session.query(models.Chemical).all()
    spray_units = session.query(models.SprayUnit).all()
    return templates.TemplateResponse("spray_program_form.html", {
        "request": request,
        "chemicals": chemicals,
        "spray_units": spray_units,
        "program": None
    })


@router.post("/spray_programs")
async def create_spray_program(request: Request, session: Session = Depends(get_session)):
    form = await request.form()

    # Parse simple fields
    number = int(form.get("number"))
    date = form.get("date")  # string, parse to date below
    #spray_unit_id = form.get("spray_unit_id")
    #spray_unit_id = int(spray_unit_id) if spray_unit_id else None

    # Parse chemicals: keys look like chemicals[0].chemical_id, chemicals[0].mix_rate_per_100L, etc.
    chemicals = []
    index = 0
    while True:
        chem_id_key = f"chemicals[{index}].chemical_id"
        mix_rate_key = f"chemicals[{index}].mix_rate_per_100L"
        spray_rate_key = f"chemicals[{index}].water_spray_rate_per_hectare"

        if chem_id_key not in form:
            break  # no more chemicals

        chemical_id = int(form.get(chem_id_key))
        mix_rate_per_100L = float(form.get(mix_rate_key))
        water_spray_rate_per_hectare = float(form.get(spray_rate_key))

        chemicals.append(
            schemas.SprayProgramChemicalCreate(
                chemical_id=chemical_id,
                mix_rate_per_100L=mix_rate_per_100L,
                water_spray_rate_per_hectare=water_spray_rate_per_hectare,
            )
        )
        index += 1

    # Build SprayProgramCreate model (validate data)
    program_data = schemas.SprayProgramCreate(
        number=number,
        date=date,
        #spray_unit_id=spray_unit_id,
        chemicals=chemicals
    )

    # Create DB objects
    program = models.SprayProgram(
        number=program_data.number,
        date=program_data.date,
        #spray_unit_id=program_data.spray_unit_id
    )
    session.add(program)
    session.commit()  # to get program.id

    for chem in program_data.chemicals:
        program_chemical = models.SprayProgramChemical(
            spray_program_id=program.id,
            chemical_id=chem.chemical_id,
            mix_rate_per_100L=chem.mix_rate_per_100L,
            water_spray_rate_per_hectare=chem.water_spray_rate_per_hectare,
        )
        session.add(program_chemical)

    session.commit()
    return RedirectResponse(url="/spray_programs", status_code=HTTP_303_SEE_OTHER)


