from behave import *
from psa_soporte.services import TicketService
from datetime import datetime

ticketService = TicketService()


@given("Soy empleado de mesa de ayuda")
def step_impl(context):
    pass


@given('La fecha actual es "{unaFechaActual}"')
def step_impl(context, unaFechaActual):
    context.fechaActual = unaFechaActual


@when("Creo un ticket con")
def step_impl(context):
    model = {row["propiedad"]: row["valor"] for row in context.table}
    context.error = None
    try:
        context.ticket = ticketService.createTicket(
            title=model["título"],
            description=model["descripción"],
            clientId=model["IDcliente"],
            tasks=model["tareas"],
            priority=model["prioridad"],
            severity=model["severidad"],
            version=model['version'],
            employees=model["responsables"].split(","),
            deadline=datetime.fromisoformat(model["fechaDeVencimiento"]),
        )
    except Exception as error:
        context.error = error


@when(
    'Creo un ticket con fecha de vencimiento "{unaFechaDeVencimiento}" anterior a la fecha actual'
)
def step_impl(context, unaFechaDeVencimiento):
    context.error = None
    try:
        context.ticket = ticketService.createTicket(
            title="No se ve el botón de pago",
            description="Al momento de realizar el pago, el botón de pago desaparece de la pantalla",
            clientId=1,
            tasks=[1],
            priority="Alta",
            severity="s1",
            version="Version 1.0",
            employees=[1],
            deadline=datetime.fromisoformat(unaFechaDeVencimiento),
            creationDate=datetime.fromisoformat(context.fechaActual),
        )
    except Exception as error:
        context.error = error


@when('Creo un ticket con un responsable asignado con id "{id}"')
def step_impl(context, id):
    context.error = None
    try:
        context.ticket = ticketService.createTicket(
            title="No se ve el botón de pago",
            description="Al momento de realizar el pago, el botón de pago desaparece de la pantalla",
            clientId=1,
            tasks=[1],
            priority="Alta",
            severity="s1",
            version="Version 1.0",
            employees=[id],
            deadline=datetime.fromisoformat("2023-01-01"),
        )
    except Exception as error:
        context.error = error


@when("Ese responsable no se encuentra en el sistema")
def step_impl(context):
    pass


@when("Creo un ticket sin alguno de los atributos obligatorios")
def step_impl(context):
    context.error = None
    try:
        context.ticket = ticketService.createTicket(
            title=None,
            description="Al momento de realizar el pago, el botón de pago desaparece de la pantalla",
            clientId=1,
            tasks=[1],
            priority="Alta",
            severity="s1",
            version="Version 1.0",
            employees=[1],
            deadline=datetime.fromisoformat("2023-01-01"),
        )
    except Exception as error:
        context.error = error


@then("El ticket se crea correctamente")
def step_impl(context):
    print(f"\n\n\n\n{context.error}")
    assert context.error == None


@then("Se emite un error")
def step_impl(context):
    print(context.error)
    assert context.error != None


@then("El ticket no es creado")
def step_impl(context):
    pass


@then("Se le asigna un ID válido")
def step_impl(context):
    assert context.ticket.id != None


@then('El estado es "{unEstado}"')
def step_impl(context, unEstado):
    assert context.ticket.state == unEstado
