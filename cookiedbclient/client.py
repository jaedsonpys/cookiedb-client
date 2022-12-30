import requests

from . import exceptions


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
        return {'Authorization': self._token}

    def _check_database_exists(self, database: str) -> bool:
        response = requests.get(
            url=f'{self._server_ur}/database',
            headers=self._get_auth_header()
        )

        if response.status_code == 200:
            data: dict = response.json()
            databases = data['result']
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

    def open(self, database: str) -> None:
        if self._check_database_exists(database):
            self._opened_database = database
        else:
            raise exceptions.DatabaseNotFoundError(f'Database "{database}" not found')
