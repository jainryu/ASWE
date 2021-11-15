'''
Unit Test for Database Class
'''

import pytest
from server.db import Database

db = Database('database_url')


def test_get_all_leads(self):
    data = db.get_all_leads()
    row = db.engine.execute("SELECT COUNT(*) FROM thumbtack.test;")
    assert len(data) == row


def test_get_thumbtack_auth(self):
    '''
    predefined TEST user is already in the database.
    checks if the function returns the correct user_id and user_pw
    '''
    test_user_id = 'TEST'
    test_user_pw = 'TEST'
    row = db.get_thumbtack_auth('TEST')
    assert row[0] == test_user_id
    assert row[1] == test_user_pw


def test_insert_row(self):
    db.clear_test_table()
    test_data = {'test': '1000'}
    db.insert_row('unittest', 'test', test_data)
    row = db.engine.execute("SELECT * FROM unittest.test LIMIT 1;").fetchone()
    assert row == test_data


def test_insert_row_from_list(self):
    db.clear_test_table()
    test_data = ['1000']
    columns = ['test']
    db.insert_row_from_list('unittest', 'test', test_data, columns)
    row = db.engine.execute("SELECT * FROM unittest.test LIMIT 1;").fetchone()
    assert row == test_data


def test_clear_test_table(self):
    db.clear_test_table()
    count = db.engine.execute("SELECT COUNT(*) FROM unittest.test")
    assert count == 0

