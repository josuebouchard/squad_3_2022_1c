from datetime import datetime
from typing import List, Optional
from psa_soporte.database import SessionLocal, Session
from psa_soporte.models import *
from .exceptions import *
import requests

url = "https://anypoint.mulesoft.com/mocking/api/v1/sources/exchange/assets/754f50e8-20d8-4223-bbdc-56d50131d0ae/recursos-psa/1.0.0/m/api/recursos"


class TicketService:
    __slots__ = ["_employee_service"]

    def createTicket(
        self,
        title: str,
        description: str,
        clientId: int,
        versionId: int,
        tasks: List[int],
        priority,
        severity,
        employees: list,
        deadline: DateTime,
    ):
        self._assert_fields_are_not_null(
            [
                title,
                description,
                clientId,
                versionId,
                priority,
                severity,
                employees,
                deadline,
            ]
        )
        self._assert_deadline_is_valid(deadline)
        self._assert_employees_are_valid(employees)
        # self._assert_tasks_are_valid(tasks)

        db: Session
        with SessionLocal() as db:
            ticket = Ticket(
                title=title,
                description=description,
                clientId=clientId,
                versionId=versionId,
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

    def getTicket(self, ticketID: int = None) -> Optional[Ticket]:
        db: Session
        with SessionLocal() as db:
            ticket = db.query(Ticket).filter_by(id=ticketID).first()
            return ticket

    def allTickets(self, versionId: Optional[int]) -> List[Ticket]:
        db: Session
        with SessionLocal() as db:
            query = db.query(Ticket)
            if versionId is not None:
                query = query.filter_by(versionId=versionId)
            return query.all()

    def updateTicket(self, id: int, fields: dict):
        """Example: `service.updateTicket(21, {'title': 'nuevo titulo'})`"""
        assert id != None

        self._assert_fields_are_not_null(list(fields.values()))

        if "deadline" in fields:
            self._assert_deadline_is_valid(fields["deadline"])

        if "employees" in fields:
            self._assert_employees_are_valid(fields["employees"])

        if "tasks" in fields:
            self._assert_tasks_are_valid(fields["tasks"])

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

    def addEmployee(self, employeeID: int, ticketID: int):
        return self.addEmployees([employeeID], ticketID)

    def _get_valid_employee_ids(self):
        employees = requests.get(url).json()
        ids = [int(employee["legajo"]) for employee in employees]

        return ids

    def addEmployees(self, employeeIDs: list, ticketID: int):
        # employeesIDs es una lista con los ids de los empleados

        db: Session
        with SessionLocal() as db:
            ticket = db.query(Ticket).filter_by(id=ticketID).first()

            valid_ids = self._get_valid_employee_ids()
            for employeeID in employeeIDs:
                if int(employeeID) not in valid_ids:
                    raise EmployeeNotFoundException(employeeID)

                ticket.employees.append(Employee(employeeID=employeeID))
            db.commit()

    def getAllEmployeesAssignedTo(self, ticketID: int):
        db: Session
        with SessionLocal() as db:
            ids = []

            for employee in db.query(Employee).filter_by(ticketID=ticketID).all():
                ids.append(int(employee.employeeID))

            return ids

    def removeEmployeeFromTicket(self, employeeID: int, ticketID: int):
        db: Session
        with SessionLocal() as db:
            exists = (
                db.query(Employee)
                .filter_by(ticketID=ticketID, employeeID=employeeID)
                .first()
                is not None
            )
            if not exists:
                raise EmployeeNotFoundException(employeeID)

            db.query(Employee).filter_by(
                employeeID=employeeID, ticketID=ticketID
            ).delete()

            db.commit()

    # Validations

    def _assert_fields_are_not_null(self, fields) -> None:
        if None in fields:
            raise AllAtributesMustBeFilledException()

    def _assert_deadline_is_valid(
        self,
        deadline: DateTime,
        creationDate: DateTime = datetime.now(),
    ) -> None:
        if deadline < creationDate:
            raise DeadlineBeforeCreationDateException()

    def _assert_employees_are_valid(self, employees):
        if len(employees) <= 0:
            raise MustAsignAtLeastOneEmployeeException()

    def _assert_tasks_are_valid(self, tasks):
        if len(tasks) <= 0:
            raise MustAsignAtLeastOneTaskException()
