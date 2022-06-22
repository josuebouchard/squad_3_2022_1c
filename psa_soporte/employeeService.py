from .database import SessionLocal, get_session, Session
from .models import *
import requests


url = 'https://anypoint.mulesoft.com/mocking/api/v1/sources/exchange/assets/754f50e8-20d8-4223-bbdc-56d50131d0ae/recursos-psa/1.0.0/m/api/recursos'


class EmployeeService:
    def __init__(self):
        pass

    def addEmployees(self, employeesID, ticketID):
        # employeesID es una lista con los ids de los empleados
        if len(employeesID) == 0:
            raise Exception('Cannot create a ticket without any assigned person')

        employees = requests.get(url).json()
        ids = []

        for employee in employees:
            ids.append(int(employee['legajo']))

        db: Session = SessionLocal()

        for employeeID in employeesID:
            if int(employeeID) not in ids:
                raise Exception('Cannot create a ticket with an assigned person who is not in the system')

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

        exists = db.query(Employee).filter_by(ticketID=ticketID, employeeID=employeeID).first() is not None
        if not exists:
            raise Exception('Cannot remove an employee that is not assigned to that ticket')

        db.query(Employee).filter_by(employeeID=employeeID, ticketID=ticketID).delete()

        db.commit()

    def addEmployee(self, employeeID, ticketID):
        return self.addEmployees([employeeID], ticketID)