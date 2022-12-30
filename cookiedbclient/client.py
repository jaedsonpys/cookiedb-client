import requests

from . import exceptions


class CookieDBClient(object):
    def __init__(self, server_url: str) -> None:
        self._server_url = server_url
        self._login_data = {}

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
