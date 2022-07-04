class BaseValidationException(Exception):
    def __str__(self) -> str:
        return self.msg


# Concrete exceptions


class DeadlineBeforeCreationDateException(BaseValidationException):
    def __init__(self) -> None:
        self.msg = "Cannot create a ticket with a deadline before the current date"
        super().__init__(self.msg)


class MustAsignAtLeastOneEmployeeException(BaseValidationException):
    def __init__(self) -> None:
        self.msg = "Cannot create a ticket without assigning at least one employee"
        super().__init__(self.msg)


class MustAsignAtLeastOneTaskException(BaseValidationException):
    def __init__(self) -> None:
        self.msg = "Cannot create a ticket without assigning at least one task"
        super().__init__(self.msg)


class AllAtributesMustBeFilledException(BaseValidationException):
    def __init__(self) -> None:
        self.msg = "All attributes must be filled"
        super().__init__(self.msg)


class TicketNotFoundException(BaseValidationException):
    def __init__(self, ticket_id: int) -> None:
        self.ticket_id = ticket_id
        self.msg = f"There is no ticket with id {ticket_id}"
        super().__init__(self.msg)


class EmployeeNotFoundException(BaseValidationException):
    def __init__(self, employee_id: int) -> None:
        self.employee_id = employee_id
        self.msg = f"Employee with id {employee_id} not found"
        super().__init__(self.msg)


class TaskNotFoundException(BaseValidationException):
    def __init__(self, ticket_id: int, task_id: int) -> None:
        self.task_id = task_id
        self.ticket_id = ticket_id
        self.msg = f"Task with id {task_id} was not assigned to ticket {ticket_id}"
        super().__init__(self.msg)


class EmployeeAlreadyAssignedException(Exception):
    def __init__(self, employee_id: int) -> None:
        self.employee_id = employee_id
        self.msg = f"Employee with id {employee_id} is already assigned to this ticket"
        super().__init__(self.msg)