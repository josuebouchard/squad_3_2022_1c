Feature: Edición de los tickets para actualizar la información de los mismos.

    Scenario: Editar un ticket correctamente
        Given Soy empleado de mesa de ayuda
        And hay un ticket
        When consulto los tickets que se encuentran en el sistema
        Then puedo editar de cada uno de esos tickets
        |item                |nuevoValor             |
        |titulo              |nuevoTitulo            |
        |descripcion         |nuevaDescripcion       |
        |prioridad           |nuevaPrioridad         |
        |severidad           |nuevaSeveridad         |
        |responsables        |nuevosResponsables     |
        |fechaDeVencimiento  |2022-12-31             |

    Scenario: Editar un ticket con fecha de vencimiento anterior a la actual
        Given Soy empleado de mesa de ayuda
        And hay un ticket
        And "2022-01-01" es anterior a la fecha actual
        When cambio la fecha de vencimiento del ticket por "2022-01-01"
        Then se emite un error

    Scenario: Editar un ticket agregando un empleado
        Given Soy empleado de mesa de ayuda
        And hay un ticket
        And empleado de id "3" no está asignado a ese ticket
        When edito el ticket y agrego como responsable asignado a empleado de id "3"
        Then empleado de id "3" ahora está asignado a ese ticket.

    Scenario: Editar un ticket removiendo un empleado
        Given Soy empleado de mesa de ayuda
        And hay un ticket
        And empleado de id "2" está asignado a ese ticket
        When edito el ticket y remuevo como responsable asignado a empleado de id "2"
        Then empleado de id "2" ahora ya no está asignado a ese ticket.

    Scenario: Editar un ticket con responsable asignado que no se encuentra en el sistema
        Given Soy empleado de mesa de ayuda
        And hay un ticket
        When edito el ticket y agrego como responsable asignado a empleado de id "5"
        And ese empleado no se encuentra en el sistema
        Then se emite un error
