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