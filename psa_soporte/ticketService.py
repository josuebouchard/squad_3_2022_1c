from datetime import datetime
from psa_soporte.database import SessionLocal, get_session, Session
from .models import *
from psa_soporte.employeeService import EmployeeService

class TicketService:
    def _init_(self):
        pass

    def containsTicket(self, ticketID):
        db: Session = SessionLocal()
        exists = db.query(Ticket).filter_by(id=ticketID).first() is not None
        db.commit()
        return exists

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
        self.checkTicket(ticketID)
        EmployeeService().addEmployee(employeeID, ticketID)

    def getAllEmployeesAssignedTo(self, ticketID):
        self.checkTicket(ticketID)
        return EmployeeService().getAllEmployeesAssignedTo(ticketID)

    def removeEmployeeFromTicket(self, employeeID, ticketID):
        self.checkTicket(ticketID)
        EmployeeService().removeEmployeeFromTicket(employeeID, ticketID)

    def closeTicket(self, ticketID):
        self.checkTicket(ticketID)
        db: Session = SessionLocal()
        ticket = db.get(Ticket, ticketID)

        if ticket.state == "Cerrado":
            raise Exception('Cannot close a ticket that is already closed')

        ticket.state = "Cerrado"
        db.commit()

    def getState(self, ticketID):
        self.checkTicket(ticketID)
        db: Session = SessionLocal()
        return db.get(Ticket, ticketID).state

    def setTitle(self, ticketID, newTitle):
        self.checkAtribute(newTitle)
        self.checkTicket(ticketID)
        db: Session = SessionLocal()
        ticket = db.get(Ticket, ticketID)
        ticket.title = newTitle
        db.commit()
        
    def getTitle(self, ticketID):
        self.checkTicket(ticketID)
        db: Session = SessionLocal()
        return db.get(Ticket, ticketID).title

    def setDescription(self, ticketID, newDescription):
        self.checkAtribute(newDescription)
        self.checkTicket(ticketID)
        db: Session = SessionLocal()
        ticket = db.get(Ticket, ticketID)
        ticket.description = newDescription
        db.commit()

    def getDescription(self, ticketID):
        self.checkTicket(ticketID)
        db: Session = SessionLocal()
        return db.get(Ticket, ticketID).description

    def setSeverity(self, ticketID, newSeverity):
        self.checkAtribute(newSeverity)
        self.checkTicket(ticketID)
        db: Session = SessionLocal()
        ticket = db.get(Ticket, ticketID)
        ticket.severity = newSeverity
        db.commit()

    def getSeverity(self, ticketID):
        self.checkTicket(ticketID)
        db: Session = SessionLocal()
        return db.get(Ticket, ticketID).severity

    def setPriority(self, ticketID, newPriority):
        self.checkAtribute(newPriority)
        self.checkTicket(ticketID)
        db: Session = SessionLocal()
        ticket = db.get(Ticket, ticketID)
        ticket.priority = newPriority
        db.commit()

    def getPriority(self, ticketID):
        self.checkTicket(ticketID)
        db: Session = SessionLocal()
        return db.get(Ticket, ticketID).priority

    def setDeadline(self, ticketID, newDeadline):
        self.checkAtribute(newDeadline)
        self.checkTicket(ticketID)
        db: Session = SessionLocal()
        ticket = db.get(Ticket, ticketID)
        if newDeadline > datetime.now():
            ticket.deadline = newDeadline
            db.commit()
        else:
            raise Exception('A ticket cannot have a deadline before the current date')

    def getDeadline(self, ticketID):
        self.checkTicket(ticketID)
        db: Session = SessionLocal()
        return db.get(Ticket, ticketID).deadline

    def checkTicket(self, ticketID):
        if not self.containsTicket(ticketID):
            raise Exception('Cannot edit a ticket that does not exist')

    def checkAtribute(self, atribute):
        if not atribute:
            raise Exception('The new atribute must not be null')