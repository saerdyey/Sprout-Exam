## Description
Basic Restful API for employee management (CRUD) system. Created using the FastAPI framwork.

## Running the API
You can run the API using docker to automatically create the dependency database server without installing and configuring the actual database.
Alternatively, you can also run the API without docker, you just need to have PostgreSQL installed and a database named sprout_exam.
Then you have to create a .env that matches the credentials you set on that database. Check .env.example file for your reference.

---


## Running with docker using docker compose
```bash
# watch mode
$ docker compose up

# detached mode
$ docker compose up -d
```

---


## Running the app without using docker
> [!NOTE]
> (Recommended) You might also want to create venv (virtual environment) before running the installation of requirements.

## Installation of requirements
```bash
$ pip install -r requirements.txt
```

## Running the app
```bash
# development
$ uvicorn app.main:app

# watch mode
$ uvicorn app.main:app --reload
```
