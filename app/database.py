from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError(
        "DATABASE_URL environment variable is not set. "
        "Please set it in Render dashboard or render.yaml."
    )

engine = create_engine(database_url, echo=False, future=True)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
