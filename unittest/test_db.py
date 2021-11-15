'''
Unit Test for Database Class
'''

import pytest
from server.db import Database

db = Database('postgresql+psycopg2://postgres:postgres@35.238.149.103/tp')


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


def test_run_sql(self):
    db.clear_test_table()
    val = '1000'
    db.engine.execute("INSERT INTO unittest.test VALUES('1000');")
    query = "SELECT * FROM unittest.test LIMIT 1;".fetchone()
    res = db.run_sql(query)
    assert val == res


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


def test_get_data():
    db.clear_test_table()
    db.engine.execute("INSERT INTO unittest.test VALUES('1000');")
    res = db.get_data(db_schema='unittest', table_name='test')
    assert '1000' == res


def test_clear_test_table(self):
    db.clear_test_table()
    count = db.engine.execute("SELECT COUNT(*) FROM unittest.test")
    assert count == 0

