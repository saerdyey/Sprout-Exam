from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, UUID
import enum
import uuid

from database import Base

class Status(enum.Enum):
    regular = 'regular'
    contractual = 'contractual'

class Employee(Base):
    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    status = Column(Enum(Status))
    number_of_leaves = Column(Integer)
    benefits = Column(ARRAY(String))
    contract_end_date = Column(Date)
    project = Column(String)