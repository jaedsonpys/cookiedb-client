# Copyright 2023 Jaedson Silva
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class ServerUnreachableError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


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
