from psa_soporte.database import SessionLocal, Session
from psa_soporte.models import Employee
from .exceptions import InvalidEmployee
import requests


url = "https://anypoint.mulesoft.com/mocking/api/v1/sources/exchange/assets/754f50e8-20d8-4223-bbdc-56d50131d0ae/recursos-psa/1.0.0/m/api/recursos"


def _get_valid_employee_ids():
    employees = requests.get(url).json()
    ids = [int(employee["legajo"]) for employee in employees]

    return ids


class EmployeeService:
    def addEmployee(self, employeeID, ticketID):
        return self.addEmployees([employeeID], ticketID)

    def addEmployees(self, employeesIDs, ticketID):
        # employeesIDs es una lista con los ids de los empleados
        if len(employeesIDs) == 0:
            raise Exception("Cannot create a ticket without any assigned person")

        db: Session = SessionLocal()

        valid_ids = _get_valid_employee_ids()

        for employeeID in employeesIDs:
            if int(employeeID) not in valid_ids:
                raise InvalidEmployee(employeeID)

            employee = Employee(employeeID=employeeID, ticketID=ticketID)

            db.add(employee)

        db.commit()
        db.refresh(employee)

        return True

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
