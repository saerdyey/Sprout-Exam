from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import Settings

settings = Settings()

pgdb_username = settings.pgdb_username
pgdb_password = settings.pgdb_password
pgdb_host = settings.pgdb_host
pgdb_port = settings.pgdb_port
pgdb_name = settings.pgdb_name

PGDB_URL = f'postgresql://{pgdb_username}:{pgdb_password}@{pgdb_host}:{pgdb_port}/{pgdb_name}'

engine = create_engine(PGDB_URL)
metadata = MetaData()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()