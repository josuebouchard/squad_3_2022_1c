Feature: Creación de Ticket

	Scenario: Asignar título a un nuevo ticket
		Given Hay que crear un ticket con el título "Bug visual"
		When Asigno ese título al ticket
		Then El ticket se crea con el título "Bug visual"

	Scenario: Asignar descripción a un nuevo ticket
		Given Hay que crear un ticket con la descripción "El botón desaparece al clickearlo"
		When Asigno esa descripción al ticket
		Then El ticket se crea con la descripción "El botón desaparece al clickearlo"