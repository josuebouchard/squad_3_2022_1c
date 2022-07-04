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


class EmployeeNotFoundException(BaseValidationException):
    def __init__(self, employee_id) -> None:
        self.employee_id = employee_id
        self.msg = f"Employee with id {employee_id} not found"
        super().__init__(self.msg)
