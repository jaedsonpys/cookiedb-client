class UserAlreadyExistsError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidDataError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class LoginUnsuccessfulError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DatabaseNotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ItemNotExistsError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    
class DatabaseExistsError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class NoOpenDatabaseError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
