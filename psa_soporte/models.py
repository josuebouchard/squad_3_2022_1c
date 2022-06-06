
from database import Base
from sqlalchemy import Column, Integer

class Employee(Base):
    __tablename__ = "employees"

    id = Column('id', Integer, primary_key=True)

class Ticket(Base):
    __tablename__ = "tickets"

    id=Column('id', Integer, primary_key=True)
