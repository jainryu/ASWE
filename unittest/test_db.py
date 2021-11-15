import unittest
from server.db import Database

db = Database('database_url')

class Test_TestDatabase(unittest.TestCase):
    # schema: unittest
    # table name: test
    # column name: name

    def test_get_all_leads(self):
        data = db.get_all_leads()
        row = db.engine.execute("SELECT COUNT(*) FROM thumbtack.test;")
        self.assertEqual(len(data), row)

    def test_get_thumbtack_auth(self):
        # TEST user should be included in the user table
        test_user_id = 'TEST'
        test_user_pw = 'TEST'
        row = db.get_thumbtack_auth('TEST')
        self.assertEqual(row[0], test_user_id)
        self.assertEqual(row[1], test_user_pw)

    def test_insert_row(self):
        db.clear_test_table()
        test_data = {'test': '1000'}
        db.insert_row('unittest', 'test', test_data)
        move = db.engine.execute("SELECT * FROM unittest.test LIMIT 1;").fetchone()
        self.assertEqual(move, test_data)

    def test_insert_row_from_list(self):
        db.clear_test_table()
        test_data = ['1000']
        columns = ['test']
        db.insert_row_from_list('unittest', 'test', test_data, columns)
        move = db.engine.execute("SELECT * FROM unittest.test LIMIT 1;").fetchone()
        self.assertEqual(move, test_data)

    def test_clear_test_table(self):
        db.clear_test_table()
        count = db.engine.execute("SELECT COUNT(*) FROM unittest.test")
        self.assertEqual(0, count)

