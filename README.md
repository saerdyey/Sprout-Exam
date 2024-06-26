## Description
Basic Restful API for employee management (CRUD) system. Created using the FastAPI framework.

## Running the API
You can run the API using docker to automatically create the dependency database server without installing and configuring the actual database.
Alternatively, you can also run the API without docker, you just need to have PostgreSQL installed and a database named sprout_exam.

You also have to create a .env file containing variables that matches the credentials you set on that database. Check .env.example file for your reference. You don't have to change the PGDB credentials if you're running it with docker compose.

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
> (Recommended) You might also want to create and activate venv (virtual environment) before running the installation of requirements.

## Creating and activating venv
for linux
```bash
# creating venv
$ python -m venv venv

# activating venv
$ source venv/bin/activate
```

for windows
```bash
# creating venv
$ python -m venv venv

# activating venv
$ venv\Scripts\activate
```


## Installation of requirements
```bash
$ pip install -r requirements.txt
```
you might encounter having issue installing the requirements in windows because of uvloop lib doesn't support windows yet, you can comment that out in the requirements.txt file.

## Running the app
```bash
# development
$ uvicorn app.main:app

# watch mode
$ uvicorn app.main:app --reload
```

## If we are
going to deploy this on production, I'd like to prioritize security. I already implemented JWT token here, but the credentials are just static, we should consider having a database or table for admin credentials with hashed passwords. We could also add validations and sanitizations of user inputs using dependencies to prevent attacks. More importantly, enforce HTTPS for secure communication.

For scalability, this is just a simple crud but if we need to add more models and services we could optimize database queries and explore caching. Currently we need to use localhost PostgreSQL database if we're running the API without using the docker, but we can also use cloud databases. For dockerized version, I didn't implement a volume setup, so we need to setup it for the data to persist even if the container is removed. We could also add API monitoring feature with comprehensive logging. Though Fast API already provides auto error handling, we can add more try except for expected possible errors to have more comprehensive logs.

Additionally, we should write unit tests to ensure individual parts of our code function as expected. This will catch bugs early in the development process and make refactoring and future development safer.

Lastly, we can also implement CICD pipelines, to automate the deployment of the API and minimize human error while maintaining a consistent process.

These are the key enhancements I think will solidify the system's security, performance, and maintainability for a smooth production deployment.
