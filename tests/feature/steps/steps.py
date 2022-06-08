from behave import *
import sys
sys.path.insert(0, '/home/ignacio/Desktop/squad_3_2022_1c/psa_soporte')

from models import *

TÍTULO = 'un título'
DESCRIPCIÓN = 'una descripción'
VENCIMIENTO = 'una fecha'
RESPONSABLES = 'unos responsables'
PRIORIDAD = 'una prioridad'
SEVERIDAD = 'una severidad'

@given(u'Hay que crear un ticket con el título "{título}"')
def step_impl(context, título):
    context.título = título


@when(u'Asigno ese título al ticket')
def step_impl(context):
    context.ticket = Ticket(context.título, DESCRIPCIÓN, VENCIMIENTO, RESPONSABLES, PRIORIDAD, SEVERIDAD)


@then(u'El ticket se crea con el título "{título}"')
def step_impl(context, título):
    assert context.ticket.obtenerTítulo() == título

@given(u'Hay que crear un ticket con la descripción "{descripción}"')
def step_impl(context, descripción):
    context.descripción = descripción


@when(u'Asigno esa descripción al ticket')
def step_impl(context):
    context.ticket = Ticket(TÍTULO, context.descripción, VENCIMIENTO, RESPONSABLES, PRIORIDAD, SEVERIDAD)


@then(u'El ticket se crea con la descripción "{descripción}"')
def step_impl(context, descripción):
    assert context.ticket.obtenerDescripción() == descripción
