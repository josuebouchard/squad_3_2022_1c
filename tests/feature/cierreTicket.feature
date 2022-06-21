Feature: Cierre de un ticket para indicar que se resolvió el problema.

    Scenario: Cuando se cierra un ticket se lo puede reabrir
        Given Soy empleado de mesa de ayuda
        And hay un ticket
        When se cambia el estado del ticket
        Then se puede cambiar el estado del ticket
        
    # No implementado por ser un test de integración
    # Escenario: Cuando se cierra un ticket no se cierran las tareas asignadas
    #     Dado que soy empleado de mesa de ayuda
    #     Y hay un ticket "#2 - Interfaz bloqueada"
    #     Y hay una tarea "#5 - cambiar boton"
    #     Y la tarea "#5 - cambiar boton" esta asignada al ticket "#2 - Interfaz bloqueada"
    #     Cuando ciero el ticket "#2 - Interfaz bloqueada"
    #     Entonces no se debe cerrar la tarea "#5 - cambiar boton"
