from sqlalchemy import *
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    taskId = Column(Integer)  # Remote foreign key to proyect system
    ticketId = Column(ForeignKey("tickets.id"))


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    employeeID = Column(Integer)  # Remote foreign key to employees system
    ticketID = Column(ForeignKey("tickets.id"))


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    clientId = Column(Integer)  # Remote foreign key to clients system

    priority = Column(String)
    severity = Column(String)
    state = Column(String, default="Abierto")
    version = Column(String)
    deadline = Column(DateTime)
    lastUpdateDate = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
    )
    creationDate = Column(DateTime(timezone=False), server_default=func.now())

    tasks = relationship("Task", lazy="joined")
    employees = relationship("Employee")
