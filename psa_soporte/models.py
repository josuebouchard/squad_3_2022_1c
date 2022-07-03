from sqlalchemy import *
from sqlalchemy.sql import func
from .database import Base
from .constants import *


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    employeeID = Column(Integer)  # Remote foreign key to employees system
    ticketID = Column(ForeignKey("tickets.id"))


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    clientId = Column(Integer)  # Remote foreign key to clients system
    title = Column(String)
    description = Column(String)
    priority = Column(String)
    severity = Column(String)
    state = Column(String, default="Abierto")
    lastUpdateDate = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
    )
    creationDate = Column(DateTime(timezone=False), server_default=func.now())
    deadline = Column(DateTime)
