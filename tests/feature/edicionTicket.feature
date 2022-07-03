Feature: Edición de los tickets para actualizar la información de los mismos.

    Scenario: Editar un ticket correctamente
        Given Soy empleado de mesa de ayuda
        And hay un ticket
        When consulto los tickets que se encuentran en el sistema
        Then puedo editar de cada uno de esos tickets
        | item              | nuevoValor                                  |
        | titulo     		| Entidades desaparecidas 					  |
        | descripcion   	| Desaparecieron entidades de mi inventario   |
        | prioridad     	| Alta 		  							      |
        | severidad 		| s3 		  							      |
        | producto 			| Sistema de inventarios versión 1.1.3	      |
        | responsables 		| 1,2                						  |
        | fechaDeVencimiento| 2023-07-07 								  |

    Scenario: Editar un ticket con fecha de vencimiento anterior a la actual
        Given Soy empleado de mesa de ayuda
        And hay un ticket
        And "2022-01-01" es anterior a la fecha actual
        When cambio la fecha de vencimiento del ticket por "2022-01-01"
        Then Se emite un error

    Scenario: Editar un ticket agregando un empleado
        Given Soy empleado de mesa de ayuda
        And hay un ticket
        And empleado de id "3" no está asignado a ese ticket
        When edito el ticket y agrego como responsable asignado a empleado de id "3"
        Then empleado de id "3" ahora está asignado a ese ticket.

    Scenario: Editar un ticket removiendo un empleado
        Given Soy empleado de mesa de ayuda
        And hay un ticket
        And empleado de id "1" está asignado a ese ticket
        When edito el ticket y remuevo como responsable asignado a empleado de id "1"
        Then empleado de id "1" ahora ya no está asignado a ese ticket.

    Scenario: Editar un ticket con responsable asignado que no se encuentra en el sistema
        Given Soy empleado de mesa de ayuda
        And hay un ticket
        When edito el ticket y agrego como responsable asignado a empleado de id "5"
        And ese empleado no se encuentra en el sistema
        Then Se emite un error

	Scenario: Editar un ticket sin un atributo
		Given Soy empleado de mesa de ayuda
		And hay un ticket
        When edito el ticket y agrego un atributo nulo
		Then Se emite un error