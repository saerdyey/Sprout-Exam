from typing import Union, List

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from enum import Enum
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine) # MIGRATION

class Status(str, Enum):
    regular = 'REGULAR'
    contractual = 'CONTRACTUAL'

class Benefits(str, Enum):
    hmo = 'HMO'
    sss = 'SSS'
    pag_ibig = 'PAG IBIG'

class Employee(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    status: Status
    number_of_leaves: int
    benefits: List[Benefits]
    contract_end_date: str
    project: str


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/employee/")
async def create_employee(employee: Employee):
    return employee

def get_db():
    db = SessionLocal()
    try:
        yield
    finally:
        db.close()