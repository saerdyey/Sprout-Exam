from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from app.models import employee
from app.models.employee import Employee
from app.database import engine
from app.dto.employee import CreateEmployeeDto
from app.dependencies import verify_token

employee.Base.metadata.create_all(bind=engine)

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]


# CREATE EMPLOYEE
@router.post("/employees/", tags=["employees"])
async def create_employee(employee: CreateEmployeeDto, db: db_dependency, username: Annotated[str, Depends(verify_token)]):
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

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return employee

# GET ALL EMPLOYEES
@router.get("/employees/", tags=["employees"])
async def get_employees(skip: int=0, limit: int=100, db: db_dependency=None, username: Annotated[str, Depends(verify_token)]=None):
    db_employees = db.query(Employee).offset(skip).limit(limit).all()

    return db_employees

# GET EMPLOYEE BY ID
@router.get("/employees/{id}", tags=["employees"])
async def get_employee(id: str, db: db_dependency, username: Annotated[str, Depends(verify_token)]):
    db_employee = db.query(Employee).filter_by(id = id).first()

    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return db_employee


# DELETE EMPLOYEE BY ID
@router.delete("/employees/{id}", tags=["employees"])
async def remove_employee(id: str, db: db_dependency, username: Annotated[str, Depends(verify_token)]):
    db_employee = db.query(Employee).filter_by(id = id).first()

    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(db_employee)
    db.commit()

    return JSONResponse(status_code=200, content={"message": "Employee deleted successfully"})

# UPDATE EMPLOYEE BY ID
@router.put("/employees/{id}", tags=["employees"])
async def update_employee(id: str, update_data: dict, db: db_dependency, username: Annotated[str, Depends(verify_token)]):
    db_employee = db.query(Employee).filter_by(id = id).first()

    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for field, value in update_data.items():

        if (field == 'status' and value == 'regular'):
            setattr(db_employee, 'contract_end_date', None)
            setattr(db_employee, 'project', None)

        elif (field == 'status' and value == 'contractual'):
            setattr(db_employee, 'benefits', None)
            setattr(db_employee, 'number_of_leaves', 0)

        if hasattr(db_employee, field):
            setattr(db_employee, field, value)
        else:
            raise HTTPException(status_code=400, detail=f"Invalid field: {field}")

    db.commit()
    db.refresh(db_employee)

    return db_employee