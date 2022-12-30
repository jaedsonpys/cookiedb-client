import sys

import bupytest

sys.path.insert(0, './')

from cookiedbclient import client


class TestClient(bupytest.UnitTest):
    def __init__(self):
        super().__init__()
        self._db = client.CookieDBClient('http://127.0.0.1:5500')


if __name__ == '__main__':
    bupytest.this()
