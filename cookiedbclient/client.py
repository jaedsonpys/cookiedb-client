from functools import wraps
from typing import Any

import requests

from . import exceptions


def open_database_required(method):
    @wraps(method)
    def wrapper(ref, *args, **kwargs):
        if ref._opened_database:
            return method(ref, *args, **kwargs)
        else:
            raise exceptions.NoOpenDatabaseError('No open database')

    return wrapper


def update_auth_token(method):
    @wraps(method)
    def wrapper(ref, *args, **kwargs):
        response = requests.get(
            url=f'{ref._server_url}/checkout',
            headers=ref._get_auth_header()
        )
            
        if response.status_code == 401:
            email, password = ref._login_data.values()
            ref.login(email, password)

        return method(ref, *args, **kwargs)

    return wrapper


class CookieDBClient(object):
    def __init__(self, server_url: str) -> None:
        self._server_url = server_url
        self._login_data = {}

        self._opened_database = None
        self._token = None

    def ping(self) -> bool:
        try:
            requests.get(self._server_url + '/')
        except requests.exceptions.ConnectionError:
            return False
        else:
            return True

    def _get_auth_header(self) -> dict:
        return {'Authorization': f'Bearer {self._token}'}

    @update_auth_token
    def list_databases(self) -> list:
        response = requests.get(
            url=f'{self._server_url}/database',
            headers=self._get_auth_header()
        )

        if response.status_code == 200:
            data: dict = response.json()
            return data['result']

    def _check_database_exists(self, database: str) -> bool:
        databases = self.list_databases()
        return database in databases

    def register(self, username: str, email: str, password: str) -> None:
        if all([username, email, password]):
            response = requests.post(self._server_url + '/register', json={
                'username': username,
                'email': email,
                'password': password
            })

            if response.status_code == 201:
                data: dict = response.json()
                status, token = data.values()

                self._login_data['email'] = email
                self._login_data['password'] = password
                self._token = token
            elif response.status_code == 409:
                raise exceptions.UserAlreadyExistsError(f'Email "{email}" already used')
        else:
            raise exceptions.InvalidDataError('Username, email and password required')

    def login(self, email: str, password: str) -> None:
        if all([email, password]):
            response = requests.post(self._server_url + '/login', json={
                'email': email,
                'password': password
            })

            if response.status_code == 201:
                data: dict = response.json()
                status, token = data.values()

                self._login_data['email'] = email
                self._login_data['password'] = password
                self._token = token
            elif response.status_code == 401:
                raise exceptions.LoginUnsuccessfulError('Email or password incorrect')
        else:
            raise exceptions.InvalidDataError('Email and password required')

    def checkout(self) -> str:
        return self._opened_database

    @update_auth_token
    def open(self, database: str) -> None:
        if self._check_database_exists(database):
            self._opened_database = database
        else:
            raise exceptions.DatabaseNotFoundError(f'Database "{database}" not found')
    
    @update_auth_token
    def create_database(self, database: str, if_not_exists: bool = False) -> None:
        response = requests.post(
            url=f'{self._server_url}/database',
            headers=self._get_auth_header(),
            json={'databaseName': database}
        )

        if response.status_code == 409 and not if_not_exists:
            raise exceptions.DatabaseExistsError(f'Database "{database}" already exists')

    @update_auth_token
    def delete_database(self, database: str) -> None:
        response = requests.delete(
            url=f'{self._server_url}/database',
            headers=self._get_auth_header(),
            json={'databaseName': database}
        )

        if response.status_code == 404:
            raise exceptions.DatabaseNotFoundError(f'Database "{database}" not found')

    @open_database_required
    @update_auth_token
    def add(self, path: str, value: Any) -> None:
        if all([path, value]):
            response = requests.post(
                url=f'{self._server_url}/database/{self._opened_database}',
                headers=self._get_auth_header(),
                json={'path': path, 'value': value}
            )

            if response.status_code == 404:
                raise exceptions.DatabaseNotFoundError(f'Database "{self._opened_database}" not exists')
        else:
            raise exceptions.InvalidDataError('Path and value required')

    @open_database_required
    @update_auth_token
    def get(self, path: str) -> Any:
        if path:
            response = requests.get(
                url=f'{self._server_url}/database/{self._opened_database}',
                headers=self._get_auth_header(),
                json={'path': path}
            )

            if response.status_code == 200:
                data: dict = response.json()
                return data['result']
            elif response.status_code == 404:
                raise exceptions.DatabaseNotFoundError(f'Database "{self._opened_database}" not exists')
        else:
            raise exceptions.InvalidDataError('Item path required')

    @open_database_required
    @update_auth_token
    def update(self, path: str, value: Any) -> None:
        if all([path, value]):
            response = requests.put(
                url=f'{self._server_url}/database/{self._opened_database}',
                headers=self._get_auth_header(),
                json={'path': path, 'value': value}
            )

            if response.status_code == 404:
                data: dict = response.json()

                if data['message'] == 'item_not_exists_error':
                    raise exceptions.ItemNotExistsError(f'Path "{path}" not exists')
                elif data['message'] == 'database_not_exists':
                    raise exceptions.DatabaseNotFoundError(f'Database "{self._opened_database}" not exists')
        else:
            raise exceptions.InvalidDataError('Path and value required')

    @open_database_required
    @update_auth_token
    def delete(self, path: str) -> None:
        if path:
            response = requests.delete(
                url=f'{self._server_url}/database/{self._opened_database}',
                headers=self._get_auth_header(),
                json={'path': path}
            )

            if response.status_code == 404:
                raise exceptions.DatabaseNotFoundError(f'Database "{self._opened_database}" not exists')
        else:
            raise exceptions.InvalidDataError('Item path required')
