from behave import *
from psa_soporte.ticketService import TicketService
from datetime import datetime

ticketService = TicketService()


@given(u'Soy empleado de mesa de ayuda')
def step_impl(context):
    pass


@when(u'Creo un ticket con')
def step_impl(context):
    model = {row['propiedad']: row['valor'] for row in context.table}
    context.error = None
    try:
        context.ticket = ticketService.createTicket(title=model['título'], description=model['descripción'],
                                                    priority=model['prioridad'], severity=model['severidad'], deadline=datetime.fromisoformat(model['fechaDeVencimiento']))
    except Exception as error:
        context.error = error


@then(u'El ticket se crea correctamente')
def step_impl(context):
    print(context.error)
    assert context.error == None


@then(u'Se le asigna un ID válido')
def step_impl(context):
    assert context.ticket.id != None


@then(u'El estado es "Abierto"')
def step_impl(context):
    assert context.ticket.state == 'Abierto'
