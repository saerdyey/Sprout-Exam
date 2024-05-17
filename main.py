from typing import Union, List, Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr
from enum import Enum
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine) # MIGRATION

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

def get_db():
    db = SessionLocal()
    print("Database session created", db)
    try:
        yield db
    finally:
        db.close()

# Annotated[Session, Depends(get_db)] indicates that the db_dependency is a Session object provided by the get_db dependency.
# Depends(get_db) tells FastAPI to use the get_db function to provide the Session object.
db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/employees/")
async def create_employee(employee: Employee, db: db_dependency):
    db_employee=models.Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        status=employee.status,
        number_of_leaves=employee.number_of_leaves,
        benefits=employee.benefits,
        contract_end_date=employee.contract_end_date,
        project=employee.project,
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# GET ALL EMPLOYEES
@app.get("/employees/")
async def get_employees(skip: int, limit: int, db: db_dependency):
    employees = db.query(models.Employee).offset(skip).limit(limit).all()
    return employees