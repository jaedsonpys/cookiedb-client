import requests


class CookieDBClient(object):
    def __init__(self, server_url: str):
        self._server_url = server_url
        self._login_data = {}

        self._token = None
