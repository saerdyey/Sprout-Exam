from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
import enum

from database import Base

class Status(enum.Enum):
    regular = 'REGULAR'
    contractual = 'CONTRACTUAL'

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    status = Column(Enum(Status))
    number_of_leaves = Column(Integer)
    benefits = Column(ARRAY(String))
    contract_end_date = Column(Date)