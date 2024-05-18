from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from app.database import get_db
from typing import List, Annotated, Optional
from sqlalchemy.orm import Session
from enum import Enum

class Status(str, Enum):
    regular = 'regular'
    contractual = 'contractual'

class Benefits(str, Enum):
    hmo = 'HMO'
    sss = 'SSS'
    pag_ibig = 'PAG IBIG'

class EmployeeRes(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    status: Status
    number_of_leaves: int = 0
    benefits: List[Benefits] = None
    contract_end_date: Optional[str]
    project: Optional[str]

class CreateEmployeeDto(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    status: Status
    number_of_leaves: int = 0
    benefits: List[Benefits] = None
    contract_end_date: str = None
    project: str = None