import uvicorn
from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException
from psa_soporte.database import Session, get_session
from starlette.responses import RedirectResponse
from typing import List
from psa_soporte.schemas import Ticket as SchemasTicket
from psa_soporte.schemas import TicketUpdate
from uuid import uuid4
from psa_soporte.models import Employee, Ticket
from psa_soporte.ticketService import TicketService

# post ticket, get todos los ticket, get de 1 ticket, update ticket, delete ticket
tickets = []

app = FastAPI()

@app.get("/")
def index():
    return RedirectResponse(url="/docs/")

@app.get("/tickets",response_model=List[SchemasTicket])
def get_tickets(db:Session=Depends(get_session)):
        tickets = db.query(Ticket).all()
        return tickets

@app.post("/tickets",response_model=SchemasTicket)
def create_ticket(newTicket:SchemasTicket):
        ticket_service = TicketService()
        ticket_service.createTicket()
        
        

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int, db:Session=Depends(get_session)):
        ticket = db.query(Ticket).filter_by(id=ticket_id).first()
        return ticket
    


@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int,db:Session=Depends(get_session)):
        ticket = db.query(Ticket).filter_by(id=ticket_id).first()
        db.delete(ticket)
        db.commit()
        return ticket 



@app.put("/ticket/{ticket_id}", response_model=SchemasTicket)
def update_ticket(ticket_id: int, updated_ticket:TicketUpdate,db:Session=Depends(get_session)):
        ticket = db.query(Ticket).filter_by(id=ticket_id).first()
        ticket.title = updated_ticket.title
        ticket.description = updated_ticket.description
        ticket.priority = updated_ticket.priority
        ticket.severity = updated_ticket.severity
        ticket.state = updated_ticket.state
        ticket.lastUpdateDate = datetime.now()
        deadline = updated_ticket.deadline
        db.commit()
        db.refresh(ticket)
        return ticket



if __name__ == "__main__":
    uvicorn.run(app=app)

