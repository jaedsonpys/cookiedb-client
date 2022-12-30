import requests


class CookieDBClient(object):
    def __init__(self):
        self._token = None
        self._login_data = {}
