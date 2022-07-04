from behave import *
from psa_soporte.services import TicketService
from datetime import datetime


@when("consulto los tickets que se encuentran en el sistema")
def step_impl(context):
    pass


@then("puedo editar de cada uno de esos tickets")
def step_impl(context):
    model = {row["item"]: row["nuevoValor"] for row in context.table}
    context.error = None
    service = TicketService()
    ticketID = context.ticket.id

    service.updateTicket(
        ticketID,
        {
            "title": model["titulo"],
            "description": model["descripcion"],
            "severity": model["severidad"],
            "version": model['version'],
            "priority": model["prioridad"],
            "deadline": datetime.fromisoformat(model["fechaDeVencimiento"]),
        },
    )

    ticket = service.getTicket(ticketID)
    assert ticket.title == model["titulo"]
    assert ticket.description == model["descripcion"]
    assert ticket.severity == model["severidad"]
    assert ticket.version == model["version"]
    assert ticket.priority == model["prioridad"]
    assert ticket.deadline == datetime.fromisoformat(model["fechaDeVencimiento"])


@given('"{nuevaFecha}" es anterior a la fecha actual')
def step_impl(context, nuevaFecha):
    assert datetime.now() > datetime.fromisoformat(nuevaFecha)


@when('cambio la fecha de vencimiento del ticket por "{nuevaFecha}"')
def step_impl(context, nuevaFecha):
    service = TicketService()
    ticketID = context.ticket.id
    try:
        service.updateTicket(ticketID, {"deadline": datetime.fromisoformat(nuevaFecha)})
    except Exception:
        context.error = True


@given('empleado de id "{empleadoId}" no está asignado a ese ticket')
def step_impl(context, empleadoId):
    pass


@when(
    'edito el ticket y agrego como responsable asignado a empleado de id "{empleadoId}"'
)
def step_impl(context, empleadoId):
    service = TicketService()
    ticketID = context.ticket.id
    try:
        service.addEmployee(empleadoId, ticketID)
    except Exception as error:
        context.error = True


@when("ese empleado no se encuentra en el sistema")
def step_impl(context):
    pass


@then('empleado de id "{empleadoId}" ahora está asignado a ese ticket.')
def step_impl(context, empleadoId):
    service = TicketService()
    ticketID = context.ticket.id
    assert int(empleadoId) in service.getAllEmployeesAssignedTo(ticketID)


@given('empleado de id "{empleadoId}" está asignado a ese ticket')
def step_impl(context, empleadoId):
    service = TicketService()
    ticketID = context.ticket.id
    try:
        service.addEmployee(empleadoId, ticketID)
    except Exception:
        context.error = True
    assert int(empleadoId) in service.getAllEmployeesAssignedTo(ticketID)


@when(
    'edito el ticket y remuevo como responsable asignado a empleado de id "{empleadoId}"'
)
def step_impl(context, empleadoId):
    service = TicketService()
    ticketID = context.ticket.id

    service.removeEmployeeFromTicket(empleadoId, ticketID)


@then('empleado de id "{empleadoId}" ahora ya no está asignado a ese ticket.')
def step_impl(context, empleadoId):
    service = TicketService()
    ticketID = context.ticket.id

    assert int(empleadoId) not in service.getAllEmployeesAssignedTo(ticketID)


@when("edito el ticket y agrego un atributo nulo")
def step_impl(context):
    service = TicketService()
    ticketID = 1

    try:
        service.updateTicket(ticketID, {"title": None})
    except:
        context.error = True
