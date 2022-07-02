from datetime import datetime, timezone
from typing import List, Optional
from psa_soporte.database import SessionLocal, Session
from psa_soporte.models import *
from .employeeService import EmployeeService


class TicketService:
    __slots__ = ["_employee_service"]

    def __init__(self, employee_service: EmployeeService = EmployeeService()):
        self._employee_service = employee_service

    def createTicket(
        self,
        title: str,
        description: str,
        priority,
        severity,
        deadline: DateTime,
    ):
        self._assert_fields_are_not_null(
            [title, description, priority, severity, deadline]
        )
        self._assert_deadline_is_valid(deadline)

        db: Session
        with SessionLocal() as db:
            ticket = Ticket(
                title=title,
                description=description,
                priority=priority,
                severity=severity,
                deadline=deadline,
            )

            db.add(ticket)
            db.commit()
            db.refresh(ticket)

            return ticket

    def getTicket(self, ticketID: int) -> Optional[Ticket]:
        db: Session
        with SessionLocal() as db:
            ticket = db.query(Ticket).filter_by(id=ticketID).first()
            return ticket

    def allTickets(self) -> List[Ticket]:
        db: Session
        with SessionLocal() as db:
            tickets = db.query(Ticket).all()
            return tickets

    def updateTicket(self, id: int, fields: dict):
        """Example: `service.updateTicket(21, {'title': 'nuevo titulo'})`"""
        assert id != None

        self._assert_fields_are_not_null(list(fields.values()))

        if "deadline" in fields:
            self._assert_deadline_is_valid(fields["deadline"])

        db: Session
        with SessionLocal() as db:
            db.execute(select())
            db.query(Ticket).filter(Ticket.id == id).update(
                fields, synchronize_session="evaluate"
            )
            db.commit()

    def deleteTicket(self, id: int) -> bool:
        """Returns `True` if ticket was found, else returns `false`"""
        db: Session
        with SessionLocal() as db:
            ticket = db.query(Ticket).filter_by(id=id).first()
            if ticket == None:
                return False
            db.delete(ticket)
            db.commit()
            return True

    # Employee methods

    def addEmployee(self, employeeID, ticketID):
        return self._employee_service.addEmployee(employeeID, ticketID)

    def getAllEmployeesAssignedTo(self, ticketID):
        return self._employee_service.getAllEmployeesAssignedTo(ticketID)

    def removeEmployeeFromTicket(self, employeeID, ticketID):
        return self._employee_service.removeEmployeeFromTicket(employeeID, ticketID)

    # Validations

    def _assert_fields_are_not_null(self, fields) -> None:
        if None in fields:
            raise Exception("Cannot create a ticket until all atributes are filled")

    def _assert_deadline_is_valid(
        self,
        deadline,
        creationDate=datetime.today().replace(tzinfo=timezone.utc),
    ) -> None:
        if deadline < creationDate:
            raise Exception(
                "Cannot create a ticket with a deadline before the current date"
            )
