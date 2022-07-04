import json
from typing import Optional
import uvicorn
from os import environ
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from psa_soporte.services import TicketService
from psa_soporte.schemas import Ticket as SchemasTicket, TicketUpdate, TicketPost
from psa_soporte.services.exceptions import (
    BaseValidationException,
    EmployeeNotFoundException,
)
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
    out_tickets = [
        SchemasTicket(
            **{
                **ticket.__dict__,
                "tasks": [task.taskId for task in ticket.tasks],
                "employees": [employee.employeeID for employee in ticket.employees],
            }
        )
        for ticket in tickets
    ]
    return out_tickets


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


@app.get("/tickets/{ticket_id}", tags=["tickets"])
def get_ticket(ticket_id: int):
    ticket = ticket_service.getTicket(ticket_id)
    if ticket == None:
        return JSONResponse(status_code=404)

    out_ticket = SchemasTicket(
        **{
            **ticket.__dict__,
            "tasks": [task.taskId for task in ticket.tasks],
            "employees": [employee.employeeID for employee in ticket.employees],
        }
    )
    return out_ticket


@app.put("/tickets/{ticket_id}", tags=["tickets"])
def update_ticket(ticket_id: int, updated_ticket: TicketUpdate):
    ticket = ticket_service.updateTicket(ticket_id, updated_ticket.dict())
    return ticket


@app.delete("/tickets/{ticket_id}", tags=["tickets"])
def delete_ticket(ticket_id: int):
    ticket_service.deleteTicket(ticket_id)
    return JSONResponse(status_code=200)


# Employees


@app.get("/tickets/{ticket_id}/employees", tags=["employees"])
def list_employees(ticket_id: int):
    employees = ticket_service.getAllEmployeesAssignedTo(ticket_id)
    return employees


@app.post("/tickets/{ticket_id}/employees", tags=["employees"])
def add_employee(ticket_id: int, employee_id: int):
    ticket_service.addEmployee(employee_id, ticket_id)
    return JSONResponse(status_code=200)


@app.delete("/tickets/{ticket_id}/employees", tags=["employees"])
def remove_employee(ticket_id: int, employee_id: int):
    ticket_service.removeEmployeeFromTicket(employee_id, ticket_id)
    return JSONResponse(status_code=200)


# Tasks


@app.get("/tickets/{ticket_id}/tasks", tags=["tasks"])
def list_tasks(ticket_id: int):
    return ticket_service.getTasks(ticket_id)


@app.post("/tickets/{ticket_id}/tasks", tags=["tasks"])
def add_task(ticket_id: int, task_id: int):
    print(f"Adding task {task_id}")
    return ticket_service.addTask(task_id, ticket_id)


@app.delete("/tickets/{ticket_id}/task", tags=["tasks"])
def delete_task(ticket_id: int, task_id: int):
    ticket_service.removeTask(task_id, ticket_id)
    return JSONResponse(status_code=200)


# Error handler


@app.exception_handler(BaseValidationException)
def validation_error_handler(req: Request, exc: BaseValidationException):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


if __name__ == "__main__":
    uvicorn.run(app=app)


# removeEmployeeFromTicket
