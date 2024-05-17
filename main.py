from typing import Union, List, Annotated

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
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
    db_employees = db.query(models.Employee).offset(skip).limit(limit).all()
    return db_employees

# GET EMPLOYEE BY ID
@app.get("/employees/{id}")
async def get_employee(id: str, db: db_dependency):
    db_employee = db.query(models.Employee).filter_by(id = id).first()
    return db_employee

# DELETE EMPLOYEE BY ID
@app.delete("/employees/{id}")
async def remove_employee(id: str, db: db_dependency):
    db_employee = db.query(models.Employee).filter_by(id = id).first()
    db.delete(db_employee)
    db.commit()
    return db_employee

# UPDATE EMPLOYEE BY ID
@app.put("/employees/{id}")
async def update_employee(id: str, update_data: dict, db: db_dependency):
    db_employee = db.query(models.Employee).filter_by(id = id).first()

    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for field, value in update_data.items():
        if hasattr(db_employee, field):
            setattr(db_employee, field, value)
        else:
            raise HTTPException(status_code=400, detail=f"Invalid field: {field}")

    # db.up(db_employee)
    # db.commit()
    db.commit()

    return JSONResponse(status_code=200, content={"message": "Employee updated successfully"})