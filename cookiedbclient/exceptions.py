class UserAlreadyExistsError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidRegisterDataError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
