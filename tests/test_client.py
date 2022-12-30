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

        self._database = 'TestDatabase'

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
        self.assert_false(self.db.login(self._user_email, self._user_password))

    def test_connect_user_with_invalid_password(self):
        try:
            self.db.login(self._user_email, 'random-password')
        except exceptions.LoginUnsuccessfulError:
            self.assert_true(True)
        else:
            self.assert_true(False, message='Invalid password not raise exception')

    def test_create_database(self):
        self.db.create_database(self._database)

    def test_create_same_database(self):
        try:
            self.db.create_database(self._database)
        except exceptions.DatabaseExistsError:
            self.assert_true(True)
        else:
            self.assert_true(False, message='DatabaseExistsError exception not thrown')

    def test_create_database_if_not_exists(self):
        try:
            self.db.create_database(self._database, if_not_exists=True)
        except exceptions.DatabaseExistsError:
            self.assert_true(False, message='DatabaseExistsError exception thrown')
        else:
            self.assert_true(True)

    def test_open_database(self):
        try:
            self.db.open(self._database)
        except exceptions.DatabaseNotFoundError:
            self.assert_true(False, message='Created database not found')
        else:
            self.assert_true(True)

    def test_open_nonexistent_database(self):
        try:
            self.db.open('NonexistentDatabase')
        except exceptions.DatabaseNotFoundError:
            self.assert_true(True)
        else:
            self.assert_true(False, message='DatabaseNotFoundError exception not thrown')


if __name__ == '__main__':
    bupytest.this()
