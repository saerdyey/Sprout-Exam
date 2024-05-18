from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PGDB_URL = 'postgresql://postgres:password123@localhost:5432/sprout'
# PGDB_URL = 'postgresql://postgres:password123@localhost:5432/sprout'

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