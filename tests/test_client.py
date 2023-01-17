import sys
import random

import bupytest

sys.path.insert(0, './')

from cookiedbclient import client, exceptions


class TestClient(bupytest.UnitTest):
    def __init__(self):
        super().__init__()

        self.db = client.CookieDBClient()
        self._database = 'TestDatabase'

        self._item = {
            'python': {
                'level': 'easy',
                'interpreted': True
            },
            'cpp': {
                'level': 'medium',
                'interpreted': False
            }
        }

    def test_unreachable_error_connect(self):
        try:
            self.db.connect('127.0.0.5', '12345678')
        except exceptions.ServerUnreachableError:
            self.assert_true(True)
        else:
            self.assert_true(False, message='Expected a ServerUnreachableError exception')

    def test_connect(self):
        try:
            self.db.connect('127.0.0.1', '12345678')
        except exceptions.ServerUnreachableError:
            self.assert_true(False, message='Unexpected ServerUnreachableError exception')
        else:
            self.assert_true(True)

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

    def test_create_other_database(self):
        self.db.create_database('TempDatabase')

    def test_list_databases(self):
        databases = self.db.list_databases()
        self.assert_expected(databases, [self._database, 'TempDatabase'])

    def test_delete_database(self):
        try:
            self.db.delete_database('TempDatabase')
        except exceptions.DatabaseNotFoundError:
            self.assert_true(False, message='DatabaseNotFoundError exception thrown')
        else:
            self.assert_true(True)

    def test_list_databases_2(self):
        databases = self.db.list_databases()
        self.assert_expected(databases, [self._database])

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

    def test_add_item(self):
        try:
            self.db.add('languages/', self._item)
        except exceptions.DatabaseNotFoundError:
            self.assert_true(False, message='DatabaseNotFoundError exception thrown')
        else:
            self.assert_true(True)

    def test_get_item(self):
        try:
            result = self.db.get('languages/')
        except exceptions.DatabaseNotFoundError:
            self.assert_true(False, message='DatabaseNotFoundError exception thrown')
        else:
            self.assert_expected(result, self._item)

    def test_get_item_2(self):
        try:
            result = self.db.get('languages/python/level')
        except exceptions.DatabaseNotFoundError:
            self.assert_true(False, message='DatabaseNotFoundError exception thrown')
        else:
            self.assert_expected(result, self._item['python']['level'])

    def test_update_item(self):
        self._item['cpp']['level'] = 'hard'

        try:
            self.db.update('languages/cpp/level', 'hard')
        except exceptions.DatabaseNotFoundError:
            self.assert_true(False, message='DatabaseNotFoundError exception thrown')
        except exceptions.ItemNotExistsError:
            self.assert_true(False, message='ItemNotExistsError exception thrown')
        else:
            result = self.db.get('languages/')
            self.assert_expected(result, self._item)

    def test_delete_item(self):
        try:
            self.db.delete('languages/python')
        except exceptions.DatabaseNotFoundError:
            self.assert_true(False, message='DatabaseNotFoundError exception thrown')
        else:
            result = self.db.get('languages/python')
            self.assert_expected(result, None)


if __name__ == '__main__':
    bupytest.this()
