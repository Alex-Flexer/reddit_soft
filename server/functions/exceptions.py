class LoginError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to login")

    def __str__(self) -> str:
        return super().__str__()


class AmountTitlesExceptions(Exception):
    def __init__(self, amount, max_amount) -> None:
        super().__init__(f"To much titles: {amount}, maximum={max_amount}")

    def __str__(self) -> str:
        return super().__str__()
