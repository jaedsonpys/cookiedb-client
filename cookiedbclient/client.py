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

import socket

from functools import wraps
from typing import Any

from . import exceptions
from .dmp import DMP


def open_database_required(method):
    @wraps(method)
    def wrapper(ref, *args, **kwargs):
        if ref._opened_database:
            return method(ref, *args, **kwargs)
        else:
            raise exceptions.NoOpenDatabaseError('No open database')

    return wrapper


class CookieDBClient:
    def __init__(self) -> None:
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._opened_database = None

    def connect(self, host: str, password: str) -> None:
        try:
            self._client.connect((host, 2808))
        except ConnectionRefusedError:
            raise exceptions.ServerUnreachableError(f'Unable to connect to {host}:2808')
        else:
            self._client.send(password.encode())
            data = self._client.recv(1024)
            response = DMP.parse_response(data)

            if response['status'] != 'OKAY':
                raise ConnectionError('Invalid password to connect')

    def _request(self, request: dict) -> dict:
        _request = DMP.make_request(request)
        self._client.send(_request)
        response = self._client.recv(5024)

        return DMP.parse_response(response)

    def list_databases(self) -> list:
        databases = self._request({'action': 'LDB', 'path': 'None'})
        return databases['data']

    def open(self, database: str) -> None:
        databases = self.list_databases()
        if database in databases:
            self._opened_database = database
        else:
            raise exceptions.DatabaseNotFoundError('Database not exists')

    def create_database(self, database: str, if_not_exists: bool = False) -> None:
        response = self._request({'action': 'CDB', 'path': database})

        if response['message'] == 'DATABASE_EXISTS' and not if_not_exists:
            raise exceptions.DatabaseExistsError('Database already exists')

    def delete_database(self, database: str) -> list:
        self._request({'action': 'DDB', 'path': database})

    @open_database_required
    def add(self, path: str, item: Any) -> None:
        _path = f'{path}:{self._opened_database}'
        self._request({'action': 'ADD', 'path': _path, 'data': item})

    @open_database_required
    def update(self, path: str, item: Any) -> None:
        _path = f'{path}:{self._opened_database}'
        response = self._request({'action': 'UPD', 'path': _path, 'data': item})

        if response['message'] == 'item_not_exists_error':
            raise exceptions.ItemNotExistsError(f'Item "{item}" not exists')

    @open_database_required
    def get(self, path: str) -> Any:
        _path = f'{path}:{self._opened_database}'
        response = self._request({'action': 'GET', 'path': _path})
        return response['data']

    @open_database_required
    def delete(self, path: str) -> Any:
        _path = f'{path}:{self._opened_database}'
        self._request({'action': 'DEL', 'path': _path})
