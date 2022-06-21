
from logging import raiseExceptions
from .database import Base
from sqlalchemy import *
from .constants import *
from sqlalchemy.sql import func


"""
table employees
|  ticketID=2    |    employeeID = 3  |
|  ticketID=2    |    employeeID = 4  |
"""


class Employee(Base):
    __tablename__ = "employees"
    id = Column('id', Integer, primary_key=True)
    employeeID = Column('employeeid', Integer)
    ticketID = Column('ticketid', ForeignKey("tickets.id"))


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String)
    description = Column('description', String)
    priority = Column('priority', String)
    severity = Column('severity', String)
    state = Column('state', String, default='Abierto')
    lastUpdateDate = Column(DateTime(timezone=True), onupdate=func.now())
    creationDate = Column(DateTime(timezone=True), server_default=func.now())
    deadline = Column(DateTime)