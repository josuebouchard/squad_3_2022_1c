from datetime import datetime
from behave import *
from psa_soporte.services import TicketService

ticketService = TicketService()

atributos = {
    "título": "No se ve el botón de pago",
    "descripción": "Al momento de realizar el pago, el botón de pago desaparece de la pantalla",
    "IDcliente": 1,
    "tareas": [1],
    "prioridad": "Alta",
    "severidad": "s1",
    "version": 1,
    "empleados": [1],
    "producto": "Aplicación de Pagos",
    "responsables": "Juan Perez",
    "fechaDeVencimiento": "2025-01-01",
}


@given("hay un ticket")
def step_impl(context):
    context.error = None
    try:
        context.ticket = ticketService.createTicket(
            title=atributos["título"],
            description=atributos["descripción"],
            clientId=atributos["IDcliente"],
            tasks=atributos["tareas"],
            priority=atributos["prioridad"],
            severity=atributos["severidad"],
            versionId=atributos["version"],
            employees=atributos["empleados"],
            deadline=datetime.fromisoformat(atributos["fechaDeVencimiento"]),
        )
    except Exception as error:
        context.error = error


@when("se cambia el estado del ticket")
def step_impl(context):
    service = TicketService()
    ticketId = context.ticket.id

    service.updateTicket(ticketId, {"state": "Cerrado"})


@then("se puede cambiar el estado del ticket")
def step_impl(context):
    service = TicketService()
    ticketId = context.ticket.id
    ticket = service.getTicket(ticketId)

    assert ticket.state == "Cerrado"
