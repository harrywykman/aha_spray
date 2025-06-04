from pydantic import BaseModel
from datetime import date

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

