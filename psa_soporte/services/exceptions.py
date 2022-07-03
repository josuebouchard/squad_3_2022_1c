class InvalidEmployee(Exception):
    def __init__(self, employee_id) -> None:
        self.employee_id = employee_id
        self.msg = (
            "Cannot create a ticket with an assigned person who is not in the system"
        )
        super().__init__(self.msg)

    def __str__(self) -> str:
        return self.msg


class DeadlineBeforeCreationDateException(Exception):
    def __init__(self) -> None:
        self.msg = "Cannot create a ticket with a deadline before the current date"
        super().__init__(self.msg)

    def __str__(self) -> str:
        return self.msg
