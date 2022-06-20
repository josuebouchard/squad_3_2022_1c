from psa_soporte.database import SessionLocal, get_session, Session
from .models import *
import requests


url = 'https://anypoint.mulesoft.com/mocking/api/v1/sources/exchange/assets/754f50e8-20d8-4223-bbdc-56d50131d0ae/recursos-psa/1.0.0/m/api/recursos'


class EmployeeService:
    def __init__(self):
        pass

    def addEmployee(self, employeeID, ticketID):
        employees = requests.get(url).json()
        ids = []

        for employee in employees:
            ids.append(int(employee['legajo']))

        if int(employeeID) not in ids:
            raise Exception('Cannot create a ticket with an assigned person who is not in the system')

        db: Session = SessionLocal()

        employee = Employee(employeeID=employeeID, ticketID=ticketID)

        db.add(employee)
        db.commit()
        db.refresh(employee)

        return employee
