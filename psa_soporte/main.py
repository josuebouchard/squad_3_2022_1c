from curses import intrflush
from os import environ
import uvicorn
from datetime import datetime
from fastapi import Depends, FastAPI
from .database import Session, engine, get_session
from . import models
from psa_soporte.services.ticketService import TicketService
from psa_soporte.schemas import Ticket as SchemasTicket
from psa_soporte.schemas import TicketUpdate
from psa_soporte.schemas import TicketPost
from starlette.responses import RedirectResponse
from typing import List
# =========== Database initialization ==========

if environ.get("ENV", "").lower() == "dev":
    models.Base.metadata.drop_all(bind=engine)

models.Base.metadata.create_all(bind=engine)

# ==============================================

app = FastAPI()


@app.get("/")
def index():
    return RedirectResponse(url="/docs/")


@app.get("/tickets")
def get_tickets():
        ticket_service = TicketService()
        tickets = ticket_service.allTickets()
        return tickets


@app.post("/tickets", response_model=SchemasTicket)
def create_ticket(newTicket: TicketPost):
        ticket_service = TicketService()
        ticket = ticket_service.createTicket(newTicket.title, newTicket.description, newTicket.priority, newTicket.severity, newTicket.employees, newTicket.deadline)
        return ticket

    
@app.get("/tickets/{ticket_id}", response_model=SchemasTicket)
def get_ticket(ticket_id: int):
        ticket_service = TicketService()
        ticket = ticket_service.getTicket(ticket_id)
        return ticket


@app.delete("/tickets/{ticket_id}", response_model=SchemasTicket)
def delete_ticket(ticket_id: int):
        ticket_service = TicketService()
        ticket = ticket_service.deleteTicket(ticket_id)
        return ticket

@app.put("/ticket/{ticket_id}")
def update_ticket(ticket_id: int, updated_ticket:TicketUpdate):
        dict = {"title":updated_ticket.title,"description":updated_ticket.description,
                   "priority":updated_ticket.priority, "severity" : updated_ticket.severity  ,"state" : updated_ticket.state, 
                   "lastUpdateDate" : datetime.now(), "deadline" : updated_ticket.deadline }
        ticket_service = TicketService()
        ticket = ticket_service.updateTicket(ticket_id, dict)
        return ticket

@app.put("/ticket/Employees/{ticket_id}", response_model=bool)
def add_employee(ticket_id: int, employee_id:int):
        ticket_service = TicketService()
        success = ticket_service.addEmployee(employee_id, ticket_id)
        return success

@app.put("/ticket/remove_employees/{ticket_id}")
def remove_employee(ticket_id: int, employee_id:int):
        ticket_service = TicketService()
        ticket_service.removeEmployeeFromTicket(employee_id, ticket_id)

@app.get("/ticket/Employees/{ticket_id}", response_model=[])
def get_employees(ticket_id: int):
        ticket_service = TicketService()
        employees = ticket_service.getAllEmployeesAssignedTo(ticket_id)
        return employees

if __name__ == "__main__":
    uvicorn.run(app=app)





#removeEmployeeFromTicket