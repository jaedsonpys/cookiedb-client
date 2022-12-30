import sys
import random

import bupytest

sys.path.insert(0, './')

from cookiedbclient import client, exceptions


class TestClient(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

        self.db = client.CookieDBClient('http://127.0.0.1:5500')

        self._user_name = 'TestClient'
        self._user_email = f'user{str(random.randint(1000, 9999))}@mail.com'
        self._user_password = str(random.randint(10000, 99999))

    def test_register_user(self):
        self.assert_false(self.db.register(self._user_name, self._user_email, self._user_password))

    def test_register_same_user(self):
        try:
            self.db.register(self._user_name, self._user_email, self._user_password)
        except exceptions.UserAlreadyExistsError:
            self.assert_true(True)
        else:
            self.assert_true(False, message='Existing user registration does not return exception')

    def test_connect_user(self):
        self.assert_false(self.db.connect(self._user_email, self._user_password))


if __name__ == '__main__':
    bupytest.this()
