from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

db_echo = environ.get("ECHO_DB", "").lower() == "true"

engine = create_engine(environ["DATABASE_URL"], echo=db_echo)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
