from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

engine = create_engine('sqlite:///db.sqlite', echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()