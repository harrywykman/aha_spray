from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from database import Base


# Define a Vineyard class inheriting from Base
class Vineyard(Base):
    __tablename__ = 'vineyards'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String)

    spray_units = relationship("SprayUnit", back_populates="vineyard")

    @property
    def spray_records(self):
        return [record for su in self.spray_units for record in su.spray_records]

class SprayRecord(Base):
    __tablename__ = 'spray_records'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    el = Column(Integer)
    operator = Column(String(256))
    wind_speed = Column(Integer)
    wind_direction = Column(String(50))
    temp = Column(Integer)
    relative_humidity = Column(Integer)
    spray_unit_id = Column(Integer, ForeignKey('spray_units.id'), nullable=False)
    spray_program_id = Column(Integer, ForeignKey('spray_programs.id'), nullable=False)
    complete = Column(Boolean, default=True)

    spray_unit = relationship("SprayUnit", back_populates="spray_records")
    spray_program = relationship("SprayProgram", back_populates="spray_records")

""" # Define a Spray Record class inheriting from Base
class SprayRecord(Base):
    __tablename__ = 'spray_records'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    el = Column(Integer)
    operator = Column(String(256))
    wind_speed = Column(Integer)
    wind_direction = Column(String(50))
    temp = Column(Integer)
    relative_humidity = Column(Integer)
    spray_unit_id = Column(Integer, ForeignKey('spray_units.id'), nullable=False)
    spray_program_id = Column(Integer, ForeignKey('spray_programs.id'), nullable=False)
    complete = Column(Boolean, default=True) """

class SprayUnit(Base):
    __tablename__ = 'spray_units'

    id = Column(Integer, primary_key=True)
    vineyard_id = Column(Integer, ForeignKey('vineyards.id'), nullable=False)
    name = Column(String, nullable=False)

    vineyard = relationship("Vineyard", back_populates="spray_units")
    spray_records = relationship("SprayRecord", back_populates="spray_unit")
    spray_programs = relationship(
        "SprayProgram",
        secondary="spray_records",
        back_populates="spray_units",
        viewonly=True  # Because real relationship is via SprayRecord
    )


""" class SprayUnit(Base):
    __tablename__ = 'spray_units'

    id = Column(Integer, primary_key=True)
    vineyard_id = Column(Integer, ForeignKey('vineyards.id'), nullable=False)
    name = Column(String, nullable=False)

    vineyard = relationship("Vineyard", back_populates="spray_units")
    spray_programs = relationship("SprayProgram", back_populates="spray_unit")
    spray_records = relationship("SprayRecord", back_populates="spray_unit") """

class SprayProgram(Base):
    __tablename__ = 'spray_programs'

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    date = Column(Date, nullable=False)

    program_chemicals = relationship("SprayProgramChemical", back_populates="spray_program")
    spray_records = relationship("SprayRecord", back_populates="spray_program")
    spray_units = relationship(
        "SprayUnit",
        secondary="spray_records",
        back_populates="spray_programs",
        viewonly=True
    )

""" class SprayProgram(Base):
    __tablename__ = 'spray_programs'

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    # spray_unit_id = Column(Integer, ForeignKey('spray_units.id'), nullable=True)
    date = Column(Date, nullable=False)

    ##spray_unit = relationship("SprayUnit", back_populates="spray_programs")
    program_chemicals = relationship("SprayProgramChemical", back_populates="spray_program") """


class Chemical(Base):
    __tablename__ = 'chemicals'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    active_ingredient = Column(String, nullable=False)

    program_chemicals = relationship("SprayProgramChemical", back_populates="chemical")


class SprayProgramChemical(Base):
    __tablename__ = 'spray_program_chemicals'

    id = Column(Integer, primary_key=True)
    spray_program_id = Column(Integer, ForeignKey('spray_programs.id'), nullable=False)
    chemical_id = Column(Integer, ForeignKey('chemicals.id'), nullable=False)
    mix_rate_per_100L = Column(Float, nullable=False)
    water_spray_rate_per_hectare = Column(Float, nullable=False)

    spray_program = relationship("SprayProgram", back_populates="program_chemicals")
    chemical = relationship("Chemical", back_populates="program_chemicals")