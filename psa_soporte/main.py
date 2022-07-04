import json
from typing import Optional
import uvicorn
from os import environ
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from psa_soporte.services import TicketService
from psa_soporte.schemas import Ticket as SchemasTicket, TicketUpdate, TicketPost
from .database import engine
from . import models

# =========== Database initialization ==========

if environ.get("ENV", "").lower() == "dev":
    models.Base.metadata.drop_all(bind=engine)

models.Base.metadata.create_all(bind=engine)

# ==============================================


# TODO: add error handlers

app = FastAPI()
ticket_service = TicketService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Productos
@app.get("/products", tags=["products"])
def list_products():
    with open("productos.json") as file:
        products = json.loads(file.read())

    return products


# Tickets


@app.get("/tickets", tags=["tickets"])
def list_tickets(versionId: Optional[int] = None):
    tickets = ticket_service.allTickets(versionId=versionId)
    return tickets


@app.post("/tickets", tags=["tickets"])
def create_ticket(newTicket: TicketPost):
    ticket = ticket_service.createTicket(
        title=newTicket.title,
        description=newTicket.description,
        clientId=newTicket.clientId,
        versionId=newTicket.versionId,
        tasks=newTicket.tasks,
        priority=newTicket.priority,
        severity=newTicket.severity,
        employees=newTicket.employees,
        deadline=newTicket.deadline,
    )
    return ticket


@app.get("/tickets/{ticket_id}", response_model=SchemasTicket, tags=["tickets"])
def get_ticket(ticket_id: int):
    ticket = ticket_service.getTicket(ticket_id)
    if ticket == None:
        return Response(status_code=404)
    return ticket


@app.put("/tickets/{ticket_id}", tags=["tickets"])
def update_ticket(ticket_id: int, updated_ticket: TicketUpdate):
    ticket = ticket_service.updateTicket(ticket_id, updated_ticket.dict())
    return ticket


@app.delete("/tickets/{ticket_id}", tags=["tickets"])
def delete_ticket(ticket_id: int):
    ticket_service.deleteTicket(ticket_id)
    return Response(status_code=200)


# Employees


@app.get("/tickets/{ticket_id}/employees", tags=["employees"])
def list_employees(ticket_id: int):
    employees = ticket_service.getAllEmployeesAssignedTo(ticket_id)
    return employees


@app.post("/tickets/{ticket_id}/employees/{employee_id}", tags=["employees"])
def add_employee(ticket_id: int, employee_id: int):
    ticket_service.addEmployee(employee_id, ticket_id)
    return Response(status_code=200)


@app.delete("/tickets/{ticket_id}/employees/{employee_id}", tags=["employees"])
def remove_employee(ticket_id: int, employee_id: int):
    ticket_service.removeEmployeeFromTicket(employee_id, ticket_id)
    return Response(status_code=200)


if __name__ == "__main__":
    uvicorn.run(app=app)


# removeEmployeeFromTicket
