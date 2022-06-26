from behave import *
from psa_soporte.ticketService import TicketService
from datetime import datetime

ticketService = TicketService()

atributos = {
    "título": "No se ve el botón de pago",
    "descripción": "Al momento de realizar el pago, el botón de pago desaparece de la pantalla",
    "prioridad": "Alta",
    "severidad": "s1",
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
            priority=atributos["prioridad"],
            severity=atributos["severidad"],
            employees=atributos["empleados"],
            deadline=datetime.fromisoformat(atributos["fechaDeVencimiento"]),
        )
    except Exception as error:
        print(error)
        context.error = error


@when("se cambia el estado del ticket")
def step_impl(context):
    service = TicketService()
    ticketId = context.ticket.id

    service.closeTicket(ticketId)


@then("se puede cambiar el estado del ticket")
def step_impl(context):
    service = TicketService()
    ticketId = context.ticket.id

    assert service.getState(ticketId) == "Cerrado"
