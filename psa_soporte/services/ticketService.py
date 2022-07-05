from datetime import datetime, timezone
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
                ticket.tasks.append(Task(taskId=taskID))

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

        # if "tasks" in fields:
        #     self._assert_tasks_are_valid(fields["tasks"])

        tasksDesired = fields.pop("tasks", [])
        employeesDesired = fields.pop("employees", [])

        db: Session
        with SessionLocal() as db:
            db.query(Ticket).filter(Ticket.id == id).update(
                fields, synchronize_session="evaluate"
            )
            db.commit()

            # Manage tasks
            db.query(Task).filter(
                Task.ticketId == id,
                Task.taskId.not_in(tasksDesired),
            ).delete(synchronize_session="fetch")
            for task in tasksDesired:
                if not db.query(Task).filter_by(ticketId=id, taskId=task).first():
                    db.add(Task(ticketId=id, taskId=task))

            db.commit()

            # Manage employees
            db.query(Employee).filter(
                Employee.ticketID == id,
                Employee.employeeID.not_in(employeesDesired),
            ).delete(synchronize_session="fetch")
            for employee in employeesDesired:
                if not db.query(Employee).filter_by(employeeID=employee).first():
                    raise EmployeeNotFoundException(employee)
                if not (
                    db.query(Employee)
                    .filter(
                        Employee.ticketID == id,
                        Employee.employeeID == employee,
                    )
                    .first()
                ):
                    db.add(Employee(ticketID=id, employeeID=employee))

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

    def _get_valid_employee_ids(self):
        employees = requests.get(url).json()
        ids = [int(employee["legajo"]) for employee in employees]

        return ids

    def getAllEmployeesAssignedTo(self, ticketID: int):
        ticket = self.getTicket(ticketID)
        if ticket is None:
            raise TicketNotFoundException(ticketID)

        return ticket.employees

    def addEmployee(self, employeeID: int, ticketID: int):
        return self.addEmployees([employeeID], ticketID)

    def addEmployees(self, employeeIDs: List[int], ticketID: int):
        # employeesIDs es una lista con los ids de los empleados

        db: Session
        with SessionLocal() as db:
            ticket = self.getTicket(ticketID)
            if ticket is None:
                raise TicketNotFoundException(ticketID)

            db.add(ticket)

            valid_ids = self._get_valid_employee_ids()
            for employeeID in employeeIDs:
                if int(employeeID) not in valid_ids:
                    raise EmployeeNotFoundException(employeeID)

                ticket.employees.append(Employee(employeeID=employeeID))
            db.commit()

    def removeEmployeeFromTicket(self, employeeID: int, ticketID: int):
            db: Session
            with SessionLocal() as db:
                
                valid_ids = self._get_valid_employee_ids()
                if int(employeeID) not in valid_ids:
                    raise EmployeeNotFoundException(employeeID)
                
                ticket = self.getTicket(ticketID)
                if ticket is None:
                    raise TicketNotFoundException(ticketID)

                self._assert_employees_are_more_than_one(ticket.employees)

                affected_rows = (
                    db.query(Employee)
                    .filter_by(
                        employeeID=employeeID,
                        ticketID=ticketID,
                    )
                    .delete()
                )


                db.commit()

        # if affected_rows <= 0:
        #     raise EmployeeNotFoundException(employeeID)

    # tasks

    def getTasks(self, ticketID: int):
        ticket = self.getTicket(ticketID)
        if ticket is None:
            raise TicketNotFoundException(ticketID)

        return ticket.tasks

    def addTask(self, taskID: int, ticketID: int):
        return self.addTasks([taskID], ticketID)

    def addTasks(self, taskIDs: List[int], ticketID: int):
        db: Session
        with SessionLocal() as db:
            ticket = self.getTicket(ticketID)
            if ticket is None:
                raise TicketNotFoundException(ticketID)

            db.add(ticket)

            for taskId in taskIDs:
                # TODO: add validation
                ticket.tasks.append(Task(taskId=taskId))
            db.commit()

    def removeTask(self, taskID: int, ticketID: int):
        db: Session
        with SessionLocal() as db:
            affected_rows = (
                db.query(Task)
                .filter_by(
                    taskId=taskID,
                    ticketId=ticketID,
                )
                .delete()
            )
            db.commit()

        # if affected_rows <= 0:
        #     raise TaskNotFoundException(ticketID, taskID)

    # Validations

    def _assert_fields_are_not_null(self, fields) -> None:
        if None in fields:
            raise AllAtributesMustBeFilledException()

    def _assert_deadline_is_valid(
        self,
        deadline: DateTime,
        creationDate: DateTime = datetime.now(),
    ) -> None:
        if deadline.replace(tzinfo=timezone.utc) < creationDate.replace(
            tzinfo=timezone.utc
        ):
            raise DeadlineBeforeCreationDateException()

    def _assert_employees_are_valid(self, employees):
        if len(employees) <= 0:
            raise MustAsignAtLeastOneEmployeeException()

    def _assert_tasks_are_valid(self, tasks):
        if len(tasks) <= 0:
            raise MustAsignAtLeastOneTaskException()

    def _assert_employees_are_more_than_one(self, employees):
        if len(employees) <= 1:
            raise MustRemainAtLeastOneEmployeeAssignedToTheTicketException()
