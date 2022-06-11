Feature: Cierra de ticket

	Scenario: Cierro un ticket
	Given: Soy empleado de mesa de ayuda y el problema fue resuelto
	When: Cierro el ticket
	Then: La tarea asociada al ticket no se cierra


	Scenario: Reabro un ticket cerrado
	Given: Soy empleado de mesa de ayuda y quiero abrir nuevamente un ticket cerrado
	When: Abro un ticket que fue cerrado
	Then: El estado del ticket es abierto
	