import unittest
from db import Database


class Test_TestDatabase(unittest.TestCase):
    # schema: unittest
    # table name: test
    # column name: name
    def setUp(self) -> None:
        self.db = Database('postgresql+psycopg2://postgres:postgres@35.238.149.103/tp')
        create_unit_test_table = '''create table if not exists talking_potato.unit_test(id varchar, name varchar);'''
        self.db.engine.execute(create_unit_test_table)
        self.db_schema = 'talking_potato'
        self.table_name = 'unit_test'

    def tearDown(self):
        drop_unit_test_table = '''drop table talking_potato.unit_test;'''
        self.db.engine.execute(drop_unit_test_table)
        self.db = None

    def test_get_thumbtack_auth(self):
        expected_result = [('thumbtack_partner', 'thumbt@ck!')]
        business_id = '286845156044809661'
        self.assertEqual(self.db.get_thumbtack_auth(business_id), expected_result)

    def test_run_sql(self):
        update_query = '''insert into talking_potato.unit_test values ('test', 'animeshbhasin');'''
        self.db.run_sql(update_query, commit_flag=True)
        assert True  # To make sure we reach here

        expected_result = '''[{"id":"test","name":"animeshbhasin"}]'''
        select_query = '''select * from talking_potato.unit_test ;'''
        self.assertEqual(self.db.run_sql(select_query, fetch_flag=True), expected_result)

    def test_insert_row(self):
        create_data = {
            'id': 'test',
            'name': 'animeshbhasin'
        }
        self.db.insert_row(self.db_schema, self.table_name, create_data)
        assert True  # To make sure we reach here

    def test_get_where_clause_arg(self):
        expected_clause = 'where id={} AND name={}'
        expected_args = ["'test'", "'animeshbhasin'"]
        filter_data = {
            'id': 'test',
            'name': 'animeshbhasin'
        }

        actual_clause, actual_args = self.db.get_where_clause_arg(filter_data)

        self.assertEqual(expected_clause, actual_clause)
        self.assertEqual(expected_args, actual_args)

    def test_get_data(self):
        expected_result = '''[{"id":"test","name":"animeshbhasin"}]'''
        data = {
            'id': 'test',
            'name': 'animeshbhasin'
        }
        self.db.insert_row(self.db_schema, self.table_name, data)
        actual_result = self.db.get_data(self.db_schema, self.table_name, filter_data=data)

        self.assertEqual(expected_result, actual_result)
