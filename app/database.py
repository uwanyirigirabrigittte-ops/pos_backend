from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

database_url = os.getenv("DATABASE_URL")

if not database_url:
    database_url = "postgresql://postgres:postgres@localhost:5432/pos-db"
    print("WARNING: DATABASE_URL not set, falling back to localhost")

engine = create_engine(database_url, echo=False, future=True)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
