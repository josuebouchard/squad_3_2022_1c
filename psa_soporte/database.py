import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

engine = create_engine(os.environ["DATABASE_URL"], echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()