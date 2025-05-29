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
        orm_mode = True

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
    name_slug: str

    class Config:
        orm_mode = True


class VineyardCreate(BaseModel):
    name: str
    name_slug: str