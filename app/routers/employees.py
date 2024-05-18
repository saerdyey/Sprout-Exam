from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from app.database import get_db
from typing import List, Annotated
from sqlalchemy.orm import Session
from enum import Enum

from app.models import employee
from app.database import engine

employee.Base.metadata.create_all(bind=engine)


router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

class Status(str, Enum):
    regular = 'regular'
    contractual = 'contractual'

class Benefits(str, Enum):
    hmo = 'HMO'
    sss = 'SSS'
    pag_ibig = 'PAG IBIG'

class Employee(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    status: Status
    number_of_leaves: int = 0
    benefits: List[Benefits] = None
    contract_end_date: str = None
    project: str = None

@router.post("/employees/", tags=["employees"])
async def create_employee(employee: Employee, db: db_dependency):
    # db_employee=Employee(
    #     first_name=employee.first_name,
    #     last_name=employee.last_name,
    #     email=employee.email,
    #     status=employee.status,
    #     number_of_leaves=employee.number_of_leaves,
    #     benefits=employee.benefits,
    #     contract_end_date=employee.contract_end_date,
    #     project=employee.project
    # )

    # print(db_employee)

    # db.add(db_employee)
    # db.commit()
    # db.refresh(db_employee)

    return employee

@router.get("/employees/", tags=["employees"])
async def get_employees(skip: int, limit: int, db: db_dependency):
    db_employees = db.query(Employee).offset(skip).limit(limit).all()
    return db_employees


@router.get("/employees/me", tags=["employees"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/employees/{username}", tags=["employees"])
async def read_user(username: str):
    return {"username": username}