import uvicorn
from os import environ
from datetime import datetime
from fastapi import FastAPI
from psa_soporte.services.ticketService import TicketService
from psa_soporte.schemas import Ticket as SchemasTicket, TicketUpdate, TicketPost
from starlette.responses import RedirectResponse
from .database import engine
from . import models

# =========== Database initialization ==========

if environ.get("ENV", "").lower() == "dev":
    models.Base.metadata.drop_all(bind=engine)

models.Base.metadata.create_all(bind=engine)

# ==============================================

app = FastAPI()


# Tickets


@app.get("/tickets", tags=["tickets"])
def list_tickets():
    ticket_service = TicketService()
    tickets = ticket_service.allTickets()
    return tickets


@app.post("/tickets", response_model=SchemasTicket, tags=["tickets"])
def create_ticket(newTicket: TicketPost):
    ticket_service = TicketService()
    ticket = ticket_service.createTicket(
        newTicket.title,
        newTicket.description,
        newTicket.priority,
        newTicket.severity,
        newTicket.employees,
        newTicket.deadline,
    )
    return ticket


@app.get("/tickets/{ticket_id}", response_model=SchemasTicket, tags=["tickets"])
def get_ticket(ticket_id: int):
    ticket_service = TicketService()
    ticket = ticket_service.getTicket(ticket_id)
    return ticket


@app.put("/tickets/{ticket_id}", tags=["tickets"])
def update_ticket(ticket_id: int, updated_ticket: TicketUpdate, tags=["tickets"]):
    dict = {
        "title": updated_ticket.title,
        "description": updated_ticket.description,
        "priority": updated_ticket.priority,
        "severity": updated_ticket.severity,
        "state": updated_ticket.state,
        "lastUpdateDate": datetime.now(),
        "deadline": updated_ticket.deadline,
    }
    ticket_service = TicketService()
    ticket = ticket_service.updateTicket(ticket_id, dict)
    return ticket


@app.delete("/tickets/{ticket_id}", response_model=SchemasTicket, tags=["tickets"])
def delete_ticket(ticket_id: int):
    ticket_service = TicketService()
    ticket = ticket_service.deleteTicket(ticket_id)
    return ticket


# Employees


@app.get("/tickets/{ticket_id}/employees", tags=["employees"])
def list_employees(ticket_id: int):
    ticket_service = TicketService()
    employees = ticket_service.getAllEmployeesAssignedTo(ticket_id)
    return employees


@app.post(
    "/tickets/{ticket_id}/employees/{employee_id}",
    response_model=bool,
    tags=["employees"],
)
def update_employees(ticket_id: int, employee_id: int):
    ticket_service = TicketService()
    success = ticket_service.addEmployee(employee_id, ticket_id)
    return success


@app.delete("/tickets/{ticket_id}/employees/{employee_id}", tags=["employees"])
def remove_employee(ticket_id: int, employee_id: int):
    ticket_service = TicketService()
    ticket_service.removeEmployeeFromTicket(employee_id, ticket_id)


if __name__ == "__main__":
    uvicorn.run(app=app)


# removeEmployeeFromTicket
