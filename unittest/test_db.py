import unittest
from server.db import Database

db = Database()


class Test_TestDatabase(unittest.TestCase):

    def test_get_all_leads(self):
        db.__init__('database_url')
        data = db.get_all_leads()
        row = db.engine.execute("SELECT COUNT(*) FROM thumbtack.test;")
        self.assertEqual(len(data), row)

    def test_insert_row(self):
        db.__init__('database_url')
        test_data = {'test': '1000'}
        db.insert_row('schema', 'TEST', test_data)
        move = db.engine.execute("SELECT * FROM TEST LIMIT 1;").fetchone()
        self.assertEqual(move, test_data)

    def insert_row_from_list(self):
        db.__init__('database_url')
        test_data = ['1000']
        columns = ['test']
        db.insert_row_from_list('schema', 'TEST', test_data, columns)
        move = db.engine.execute("SELECT * FROM TEST LIMIT 1;").fetchone()
        self.assertEqual(move, test_data)

