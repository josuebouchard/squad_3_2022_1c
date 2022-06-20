Feature: Creación de Ticket

	Scenario: Crear un ticket correctamente
		Given Soy empleado de mesa de ayuda
		When Creo un ticket con
			| propiedad         | valor 									  |
			| título     		| Entidades desaparecidas 					  |
			| descripción   	| Desaparecieron entidades de mi inventario   |
			| prioridad     	| Alta 		  							      |
			| severidad 		| s3 		  							      |
			| producto 			| Sistema de inventarios versión 1.1.3	      |
			| responsables 		| 1,2                						  |
			| fechaDeVencimiento| 2023-07-07 								  |
		Then El ticket se crea correctamente
		And Se le asigna un ID válido
		And El estado es "Abierto"


	Scenario: Crear un ticket con fecha de vencimiento anterior a la actual
		Given Soy empleado de mesa de ayuda
		And La fecha actual es "2022-06-20"
		When Creo un ticket con fecha de vencimiento "2023-01-01" anterior a la fecha actual
		Then Se emite un error
		And El ticket no es creado

	
	Scenario: Crear un ticket con responsable asignado que no se encuentra en el sistema
		Given Soy empleado de mesa de ayuda
		When Creo un ticket con un responsable asignado con id "1000"
		And Ese responsable no se encuentra en el sistema
		Then Se emite un error



