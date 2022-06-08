
from database import Base
from sqlalchemy import Column, Integer
from constants import *

class Employee(Base):
	__tablename__ = "employees"

	id = Column('id', Integer, primary_key=True)

class Ticket(Base):
	__tablename__ = "tickets"

	id=Column('id', Integer, primary_key=True)

	def __init__(self, título, descripción, vencimiento, responsables=[], prioridad=PRIORIDAD_ALTA, severidad=S1):
		self.título = título
		self.descripción = descripción
		self.vencimiento = vencimiento
		self.responsables = responsables
		self.prioridad = prioridad
		self.severidad = severidad

	def obtenerTítulo(self):
		return self.título

	def obtenerDescripción(self):
		return self.descripción
