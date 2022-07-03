from datetime import datetime, timezone
from typing import List, Optional
from psa_soporte.database import SessionLocal, Session
from psa_soporte.models import *
from .exceptions import DeadlineBeforeCreationDateException, InvalidEmployee
#from .employeeService import EmployeeService
import requests

url = "https://anypoint.mulesoft.com/mocking/api/v1/sources/exchange/assets/754f50e8-20d8-4223-bbdc-56d50131d0ae/recursos-psa/1.0.0/m/api/recursos"


class TicketService:
    __slots__ = ["_employee_service"]

    #def __init__(self):
        #self._employee_service = employee_service

    def createTicket(
        self,
        title: str,
        description: str,
        clientId: int,
        tasks: List[int],
        priority,
        severity,
        employees: list,
        deadline: DateTime,
    ):
        self._assert_fields_are_not_null(
            [title, description, priority, severity, employees, deadline]
        )
        self._assert_deadline_is_valid(deadline)

        db: Session
        with SessionLocal() as db:
            ticket = Ticket(
                title=title,
                description=description,
                clientId=clientId,
                priority=priority,
                severity=severity,
                deadline=deadline,
            )

            for taskID in tasks:
                ticket.tasks.append(Task(taskId=taskID, ticketId=ticket.id))

            db.add(ticket)
            db.commit()
            db.refresh(ticket)

            self.addEmployees(employees, ticket.id)

            return ticket

    def getTicket(self, ticketID: int) -> Optional[Ticket]:
        db: Session
        with SessionLocal() as db:
            ticket = db.query(Ticket).filter_by(id=ticketID).first()

            # TODO: no devolver clientId sino devolver data del cliente

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
        return self.addEmployees([employeeID], ticketID)

    def _get_valid_employee_ids(self):
        employees = requests.get(url).json()
        ids = [int(employee["legajo"]) for employee in employees]

        return ids

    def addEmployees(self, employeeIDs, ticketID):
        # employeesIDs es una lista con los ids de los empleados
        db: Session = SessionLocal()
        ticket = db.query(Ticket).get(ticketID)
        
        valid_ids = self._get_valid_employee_ids()

        for employeeID in employeeIDs:
            if int(employeeID) not in valid_ids:
                raise InvalidEmployee(employeeID)

            ticket.employees.append(Employee(employeeID=employeeID))
        db.commit()

    def getAllEmployeesAssignedTo(self, ticketID):
        db: Session = SessionLocal()
        ids = []

        for employee in db.query(Employee).filter_by(ticketID=ticketID).all():
            ids.append(int(employee.employeeID))

        return ids

    def removeEmployeeFromTicket(self, employeeID, ticketID):
        db: Session = SessionLocal()

        exists = (
            db.query(Employee)
            .filter_by(ticketID=ticketID, employeeID=employeeID)
            .first()
            is not None
        )
        if not exists:
            raise Exception(
                "Cannot remove an employee that is not assigned to that ticket"
            )

        db.query(Employee).filter_by(employeeID=employeeID, ticketID=ticketID).delete()

        db.commit()

    # Validations

    def _assert_fields_are_not_null(self, fields) -> None:
        if None in fields:
            raise Exception("Cannot create a ticket until all atributes are filled")

    def _assert_deadline_is_valid(
        self,
        deadline: DateTime,
        creationDate: DateTime = datetime.now(),
    ) -> None:
        if deadline < creationDate:
            raise DeadlineBeforeCreationDateException()
