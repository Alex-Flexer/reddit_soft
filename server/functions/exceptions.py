class LoginError(Exception):
    def __init__(self) -> None:
        super().__init__("Failed to login")

    def __str__(self) -> str:
        return super().__str__()
