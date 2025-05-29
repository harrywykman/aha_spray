from sqlalchemy import Column, Integer, String, Date
from database import Base

# Define a Spray Record class inheriting from Base
class Vineyard(Base):
    __tablename__ = 'Vineyards'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    name_slug = Column(String(256))

# Define a Spray Record class inheriting from Base
class SprayRecord(Base):
    __tablename__ = 'SprayRecords'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    el = Column(Integer)
    operator = Column(String(256))
    wind_speed = Column(Integer)
    wind_direction = Column(String(50))
    temp = Column(Integer)
    relative_humidity = Column(Integer)