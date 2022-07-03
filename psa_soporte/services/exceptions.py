class DeadlineBeforeCreationDateException(Exception):
    def __init__(self) -> None:
        self.msg = "Cannot create a ticket with a deadline before the current date"
        super().__init__(self.msg)

    def __str__(self) -> str:
        return self.msg


class MustAsignAtLeastOneEmployeeException(Exception):
    def __init__(self) -> None:
        self.msg = "Cannot create a ticket without assigning at least one employee"
        super().__init__(self.msg)

    def __str__(self) -> str:
        return self.msg


class MustAsignAtLeastOneTaskException(Exception):
    def __init__(self) -> None:
        self.msg = "Cannot create a ticket without assigning at least one task"
        super().__init__(self.msg)

    def __str__(self) -> str:
        return self.msg


class AllAtributesMustBeFilledException(Exception):
    def __init__(self) -> None:
        self.msg = "All attributes must be filled"
        super().__init__(self.msg)

    def __str__(self) -> str:
        return self.msg


class EmployeeNotFoundException(Exception):
    def __init__(self, employee_id) -> None:
        self.employee_id = employee_id
        self.msg = f"Employee with id {employee_id} not found"
        super().__init__(self.msg)

    def __str__(self) -> str:
        return self.msg