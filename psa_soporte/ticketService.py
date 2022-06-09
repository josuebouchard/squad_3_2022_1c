from psa_soporte.database import SessionLocal, get_session, Session
from .models import *


class TicketService:
    def __init__(self):
        pass

    def createTicket(self, title, description, priority, severity, deadline):
        db: Session = SessionLocal()

        ticket = Ticket(title=title, description=description,
                        priority=priority, severity=severity, deadline=deadline)

        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        return ticket 
