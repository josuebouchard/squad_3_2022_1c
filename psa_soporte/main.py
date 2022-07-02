import json
import uvicorn
from os import environ
from fastapi import FastAPI, Response
from psa_soporte.services import TicketService, InvalidEmployee
from psa_soporte.schemas import Ticket as SchemasTicket, TicketUpdate, TicketPost
from .database import engine
from . import models

# =========== Database initialization ==========

if environ.get("ENV", "").lower() == "dev":
    models.Base.metadata.drop_all(bind=engine)

models.Base.metadata.create_all(bind=engine)

# ==============================================

app = FastAPI()


# Productos
@app.get("/products", tags=["products"])
def list_products():
    with open("productos.json") as file:
        products = json.loads(file.read())

    return products


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
        newTicket.deadline,
    )
    return ticket


@app.get("/tickets/{ticket_id}", response_model=SchemasTicket, tags=["tickets"])
def get_ticket(ticket_id: int):
    ticket_service = TicketService()
    ticket = ticket_service.getTicket(ticket_id)
    return ticket


@app.put("/tickets/{ticket_id}", tags=["tickets"])
def update_ticket(ticket_id: int, updated_ticket: TicketUpdate):
    dict = {
        "title": updated_ticket.title,
        "description": updated_ticket.description,
        "priority": updated_ticket.priority,
        "severity": updated_ticket.severity,
        "state": updated_ticket.state,
        "deadline": updated_ticket.deadline,
    }
    ticket_service = TicketService()
    ticket = ticket_service.updateTicket(ticket_id, dict)
    return ticket


@app.delete("/tickets/{ticket_id}", tags=["tickets"])
def delete_ticket(ticket_id: int):
    ticket_service = TicketService()
    ticket_service.deleteTicket(ticket_id)
    return Response(status_code=200)


# Employees


@app.get("/tickets/{ticket_id}/employees", tags=["employees"])
def list_employees(ticket_id: int):
    ticket_service = TicketService()
    employees = ticket_service.getAllEmployeesAssignedTo(ticket_id)
    return employees


@app.post("/tickets/{ticket_id}/employees/{employee_id}", tags=["employees"])
def add_employee(ticket_id: int, employee_id: int):
    ticket_service = TicketService()
    try:
        ticket_service.addEmployee(employee_id, ticket_id)
    except InvalidEmployee as exception:
        return Response(content=str(exception), status_code=406)

    return Response(status_code=200)


@app.delete("/tickets/{ticket_id}/employees/{employee_id}", tags=["employees"])
def remove_employee(ticket_id: int, employee_id: int):
    ticket_service = TicketService()
    ticket_service.removeEmployeeFromTicket(employee_id, ticket_id)


if __name__ == "__main__":
    uvicorn.run(app=app)


# removeEmployeeFromTicket
