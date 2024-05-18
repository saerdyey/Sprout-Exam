from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.dialects.postgresql import ARRAY, UUID
import enum
import uuid

from app.database import Base

class StatusEnum(enum.Enum):
    regular = 'regular'
    contractual = 'contractual'

class Employee(Base):
    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    status = Column(Enum(StatusEnum))
    number_of_leaves = Column(Integer, nullable=True)
    benefits = Column(ARRAY(String), nullable=True)
    contract_end_date = Column(Date, nullable=True)
    project = Column(String, nullable=True)
    test = Column(String, nullable=True)