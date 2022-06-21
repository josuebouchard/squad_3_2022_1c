from behave import *
from psa_soporte.ticketService import TicketService
from psa_soporte.employeeService import EmployeeService
from datetime import datetime

ticketService = TicketService()


@given(u'Soy empleado de mesa de ayuda')
def step_impl(context):
    pass


@given(u'La fecha actual es "{unaFechaActual}"')
def step_impl(context, unaFechaActual):
    context.fechaActual = unaFechaActual


@when(u'Creo un ticket con fecha de vencimiento "{unaFechaDeVencimiento}" anterior a la fecha actual')
def step_impl(context, unaFechaDeVencimiento):
    context.error = None
    try:
        context.ticket = ticketService.createTicket(title='No se ve el botón de pago', description='Al momento de realizar el pago, el botón de pago desaparece de la pantalla',
                                                    priority='Alta', severity='s1', deadline=datetime.fromisoformat(unaFechaDeVencimiento), creationDate=datetime.fromisoformat(context.fechaActual))
    except Exception as error:
        context.error = error


@when(u'Creo un ticket con')
def step_impl(context):
    model = {row['propiedad']: row['valor'] for row in context.table}
    context.error = None
    try:
        context.ticket = ticketService.createTicket(title=model['título'], description=model['descripción'],
                                                    priority=model['prioridad'], severity=model['severidad'], deadline=datetime.fromisoformat(model['fechaDeVencimiento']))
    except Exception as error:
        context.error = error

    for employeeID in model['responsables'].split(','):
        try:
            EmployeeService().addEmployee(int(employeeID), context.ticket.id)

        except Exception as error:
            context.error = error


@then(u'El ticket se crea correctamente')
def step_impl(context):
    assert context.error == None


@then(u'Se emite un error')
def step_impl(context):
    assert context.error != None


@then(u'El ticket no es creado')
def step_impl(context):
    pass


@then(u'Se le asigna un ID válido')
def step_impl(context):
    assert context.ticket.id != None


@then(u'El estado es "{unEstado}"')
def step_impl(context, unEstado):
    assert context.ticket.state == unEstado


@when(u'Creo un ticket con un responsable asignado con id "{id}"')
def step_impl(context, id):
    context.error = None
    try:
        context.ticket = ticketService.createTicket(title='No se ve el botón de pago', description='Al momento de realizar el pago, el botón de pago desaparece de la pantalla',
                                                    priority='Alta', severity='s1', deadline=datetime.fromisoformat('2023-01-01'))
    except Exception as error:
        context.error = error

    try:
        EmployeeService().addEmployee(id, context.ticket.id)

    except Exception as error:
        context.error = error


@when(u'Ese responsable no se encuentra en el sistema')
def step_impl(context):
    pass

