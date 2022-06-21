from behave import *
from psa_soporte.ticketService import TicketService
from psa_soporte.employeeService import EmployeeService
from datetime import datetime

@when(u'consulto los tickets que se encuentran en el sistema')
def step_impl(context):
    pass


@then(u'puedo editar de cada uno de esos tickets')
def step_impl(context):
    model = {row['item']: row['nuevoValor'] for row in context.table}
    context.error = None
    service = TicketService()
    ticketId = context.ticket.id

    service.setTitle(ticketId, model["titulo"])
    service.setDescription(ticketId, model["descripcion"])
    service.setSeverity(ticketId, model["severidad"])
    service.setPriority(ticketId, model["prioridad"])
    service.setDeadline(ticketId, datetime.fromisoformat(model['fechaDeVencimiento']))

    assert service.getTitle(ticketId) == model["titulo"]
    assert service.getDescription(ticketId) == model["descripcion"]
    assert service.getSeverity(ticketId) == model["severidad"]
    assert service.getPriority(ticketId) == model["prioridad"]
    assert service.getDeadline(ticketId) == datetime.fromisoformat(model['fechaDeVencimiento'])



@given(u'"{nuevaFecha}" es anterior a la fecha actual')       
def step_impl(context, nuevaFecha):
    assert datetime.now() >  datetime.fromisoformat(nuevaFecha)
    


@when(u'cambio la fecha de vencimiento del ticket por "{nuevaFecha}"')
def step_impl(context, nuevaFecha):
    service = TicketService()
    ticketId = context.ticket.id
    try:
        service.setDeadline(ticketId, datetime.fromisoformat(nuevaFecha))
    except Exception:
        context.error = True


@given(u'empleado de id "{empleadoId}" no está asignado a ese ticket')
def step_impl(context, empleadoId):
    pass


@when(u'edito el ticket y agrego como responsable asignado a empleado de id "{empleadoId}"')
def step_impl(context, empleadoId):
    service = TicketService()
    ticketId = context.ticket.id
    try:
        service.addEmployee(empleadoId, ticketId)
    except Exception as error:
        context.error = True

@when(u'ese empleado no se encuentra en el sistema')  
def step_impl(context):
    pass


@then(u'empleado de id "{empleadoId}" ahora está asignado a ese ticket.')
def step_impl(context, empleadoId):
    service = TicketService()
    ticketId = context.ticket.id
    assert int(empleadoId) in service.getAllEmployeesAssignedTo(ticketId)

@given(u'empleado de id "{empleadoId}" está asignado a ese ticket')
def step_impl(context,empleadoId):
    service = TicketService()
    ticketId = context.ticket.id
    try:
        service.addEmployee(empleadoId, ticketId)
    except Exception as error:
        context.error = True

    assert int(empleadoId) in service.getAllEmployeesAssignedTo(ticketId)

@when(u'edito el ticket y remuevo como responsable asignado a empleado de id "{empleadoId}"')
def step_impl(context,empleadoId):
    service = TicketService()
    ticketId = context.ticket.id

    service.removeEmployeeFromTicket(empleadoId, ticketId)


@then(u'empleado de id "{empleadoId}" ahora ya no está asignado a ese ticket.')
def step_impl(context,empleadoId):
    service = TicketService()
    ticketId = context.ticket.id

    assert int(empleadoId) not in service.getAllEmployeesAssignedTo(ticketId)