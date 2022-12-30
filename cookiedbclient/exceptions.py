class UserAlreadyExistsError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidRegisterDataError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidLoginDataError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class LoginUnsuccessfulError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
