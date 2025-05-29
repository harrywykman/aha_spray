from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create sqlite instance
engine = create_engine("sqlite:///spray_records.db")

# Create DeclarativeMeta instance
Base = declarative_base()

# Create SessionLocal class from sessionmaker factory
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)