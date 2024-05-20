from pydantic import BaseModel, EmailStr
from typing import List, Optional
from enum import Enum

class Status(str, Enum):
    regular = 'regular'
    contractual = 'contractual'

class Benefits(str, Enum):
    hmo = 'HMO'
    sss = 'SSS'
    pag_ibig = 'PAG IBIG'

class CreateEmployeeDto(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    status: Status
    number_of_leaves: int = 0
    benefits: List[Benefits] = None
    contract_end_date: str = None
    project: str = None