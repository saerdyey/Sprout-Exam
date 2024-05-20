from fastapi import FastAPI

from .routers import employees, token


app = FastAPI()

app.include_router(employees.router)
app.include_router(token.router)

@app.get("/")
async def root():
    return {"message": "Sprout Exam by Jay Anton Roblico 🤟"}