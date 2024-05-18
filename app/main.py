from fastapi import Depends, FastAPI
from .dependencies import get_query_token, get_token_header
from .routers import employees

# app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()
# Base.metadata.create_all(bind=engine) # MIGRATION

app.include_router(employees.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}