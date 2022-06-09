Feature: Creación de Ticket

	Scenario: Crear un nuevo ticket correctamente
		Given Soy empleado de mesa de ayuda
		When Creo un ticket con
			| propiedad         | valor 																	   |
			| título     		| No se ve el botón de pago 												   |
			| descripción   	| Al momento de realizar el pago, el botón de pago desaparece de la pantalla   |
			| prioridad     	| Alta 		  																   |
			| severidad 		| s1 		  																   |
			| producto 			| Aplicación de Pagos 														   |
			| responsables 		| Juan Perez 																   |
			| fechaDeVencimiento| 2022-12-31 																   |
		Then El ticket se crea correctamente
		And Se le asigna un ID válido
		And El estado es "Abierto"


	Scenario: Creo nuevo ticket con fecha de vencimiento invalida
		Given Soy empleado de mesa de ayuda
		When Creo un ticket el dia 12-03-2022 con
			| fechaDeVencimiento| 11-03-2022 |
		Then El sistema emite el mensaje de error "Fecha de vencimiento Invalida"
		And El ticket no es creado

	Scenario: Creo ticket con un responsable que no se encuentra en el sistema
		Given Soy un emplado de mesa de ayuda y Roberto Carlos no se encuentra en el sistema
		When Creo un ticket con
			| responsables | Roberto Carlos |
		Then El sistema emite el mensaje de error "El responsable no se encuentra en el sistema"
		And El ticket no es creado

	Scenario: Creo ticket con un producto que no se encuentra en el sistema
		Given Soy un emplado de mesa de ayuda y el producto Aplicacion de Pagos no se encuentra en el sistema
		When Creo un ticket con
			| producto	| Aplicacion de pagos |
		Then El sistema emite el mensaje de error "El producto no se encuentra en el sistema"
		And El ticket no es creado


