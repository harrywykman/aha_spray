from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional, List


class SprayProgramChemicalCreate(BaseModel):
    chemical_id: int
    mix_rate_per_100L: int
    water_spray_rate_per_hectare: int

class SprayProgramBase(BaseModel):
    number: int
    spray_unit_id: int  | None = None
    date: date
    chemicals: List[SprayProgramChemicalCreate]

# Input model
class SprayProgramCreate(SprayProgramBase):
    pass

# Output model
class SprayProgramRead(SprayProgramBase):
    id: int

    model_config = ConfigDict(from_attributes=True)




# Create SprayRecord Base Model
class SprayRecord(BaseModel):
    id: int
    date: date
    el: int
    operator: str
    wind_speed: int
    wind_direction: str
    temp: int
    relative_humidity: int

    class Config:
        from_attributes = True 

# Create SprayRecordCreate Base Model
class SprayRecordCreate(BaseModel):
    date: date
    el: int
    operator: str
    wind_speed: int
    wind_direction: str
    temp: int
    relative_humidity: int


class Vineyard(BaseModel):
    id: int
    name: str
    address: str

    class Config:
        from_attributes = True 


class VineyardCreate(BaseModel):
    name: str
    address: str


class Chemical(BaseModel):
    id: int
    name: str
    active_ingredient: str

    class Config:
        from_attributes = True 


class ChemicalCreate(BaseModel):
    name: str
    active_ingredient: str

class SprayUnit(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True 

class SprayUnitCreate(BaseModel):
    pass

