from datetime import datetime
from psa_soporte.database import SessionLocal, get_session, Session
from .models import *
from psa_soporte.employeeService import EmployeeService

class TicketService:
    def _init_(self):
        pass

    def createTicket(self, title, description, priority, severity, employees, deadline, creationDate=datetime.today()):
        if None in (title, description, priority, severity, deadline):
            raise Exception('Cannot create a ticket until all atributes are filled')

        if deadline < creationDate:
            raise Exception('Cannot create a ticket with a deadline before the current date')

        db: Session = SessionLocal()

        ticket = Ticket(title=title, description=description,
                        priority=priority, severity=severity, deadline=deadline)

        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        EmployeeService().addEmployees(employees, ticket.id)

        return ticket

    def addEmployee(self, employeeID, ticketID):
        EmployeeService().addEmployee(employeeID, ticketID)

    def getAllEmployeesAssignedTo(self, ticketID):
        return EmployeeService().getAllEmployeesAssignedTo(ticketID)

    def removeEmployeeFromTicket(self, employeeID, ticketID):
        EmployeeService().removeEmployeeFromTicket(employeeID, ticketID)

    def closeTicket(self, ticketID):
        db: Session = SessionLocal()
        ticket = db.get(Ticket, ticketID)

        ticket.state = "Cerrado"
        db.commit()

    def getState(self, ticketID):
        db: Session = SessionLocal()
        return db.get(Ticket, ticketID).state

    def setTitle(self, ticketID, newTitle):
        db: Session = SessionLocal()
        ticket = db.get(Ticket, ticketID)
        ticket.title = newTitle
        db.commit()
        
    def getTitle(self, ticketID):
        db: Session = SessionLocal()
        return db.get(Ticket, ticketID).title

    def setDescription(self, ticketID, newDescription):
        db: Session = SessionLocal()
        ticket = db.get(Ticket, ticketID)
        ticket.description = newDescription
        db.commit()

    def getDescription(self, ticketID):
            db: Session = SessionLocal()
            return db.get(Ticket, ticketID).description

    def setSeverity(self, ticketID, newSeverity):
        db: Session = SessionLocal()
        ticket = db.get(Ticket, ticketID)
        ticket.severity = newSeverity
        db.commit()

    def getSeverity(self, ticketID):
            db: Session = SessionLocal()
            return db.get(Ticket, ticketID).severity

    def setPriority(self, ticketID, newPriority):
        db: Session = SessionLocal()
        ticket = db.get(Ticket, ticketID)
        ticket.priority = newPriority
        db.commit()

    def getPriority(self, ticketID):
            db: Session = SessionLocal()
            return db.get(Ticket, ticketID).priority

    def setDeadline(self, ticketID, newDeadline):
        db: Session = SessionLocal()
        ticket = db.get(Ticket, ticketID)
        if newDeadline > datetime.now():
            ticket.deadline = newDeadline
            db.commit()
        else:
            raise Exception("La fecha de vencimiento no puede ser anterior a la actual")

    def getDeadline(self, ticketID):
            db: Session = SessionLocal()
            return db.get(Ticket, ticketID).deadline
