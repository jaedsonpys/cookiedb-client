# CookieDBClient, a client to connect in CookieDB Server
# Copyright (C) 2023  Jaedson Silva

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


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
