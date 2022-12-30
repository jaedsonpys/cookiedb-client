import requests

from . import exceptions


class CookieDBClient(object):
    def __init__(self, server_url: str) -> None:
        self._server_url = server_url
        self._login_data = {}

        self._token = None

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
                self._token = token
        else:
            raise exceptions.InvalidRegisterDataError('Username, email and password required')
