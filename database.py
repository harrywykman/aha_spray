from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

# Create sqlite instance
engine = create_engine("sqlite:///spray_records.db")

# Create DeclarativeMeta instance
Base = declarative_base()

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