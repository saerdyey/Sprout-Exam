from fastapi import APIRouter, Depends
from app.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session

from app.models import employee
from app.models.employee import Employee
from app.database import engine
from app.dto.employee import CreateEmployeeDto

employee.Base.metadata.create_all(bind=engine)


router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/employees/", tags=["employees"])
async def create_employee(employee: CreateEmployeeDto, db: db_dependency):
    db_employee=Employee(
        first_name=employee.first_name,
        last_name=employee.last_name,
        email=employee.email,
        status=employee.status,
        number_of_leaves=employee.number_of_leaves,
        benefits=employee.benefits,
        contract_end_date=employee.contract_end_date,
        project=employee.project
    )

    print(db_employee)

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

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