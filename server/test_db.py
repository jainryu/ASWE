"""
unit test for db module
"""
import unittest
from db import Database


# pylint: disable=invalid-name
class TestTestDatabase(unittest.TestCase):
    """
    unit test class for db.py
    """
    def setUp(self) -> None:
        """Setup database unit testing table

        :return None
        """
        self.db_obj = Database('postgresql+psycopg2://postgres:postgres@35.238.149.103/tp')
        create_unit_test_table \
            = '''create table if not exists talking_potato.unit_test(id varchar, name varchar);'''
        self.db_obj.engine.execute(create_unit_test_table)
        self.db_schema = 'talking_potato'
        self.table_name = 'unit_test'

    def tearDown(self):
        """Tear down database unit testing table

        :return None
        """
        drop_unit_test_table = '''drop table talking_potato.unit_test;'''
        self.db_obj.engine.execute(drop_unit_test_table)
        self.db_obj = None

    def test_get_thumbtack_auth(self):
        """Unit test to test get_thumbtack_auth method

        :return None
        """
        expected_result = [('thumbtack_partner', 'thumbt@ck!')]
        business_id = '286845156044809661'
        self.assertEqual(self.db_obj.get_thumbtack_auth(business_id)[0], expected_result)

    def test_run_sql(self):
        """Unit test to test run_sql method

        :return None
        """
        update_query = '''insert into talking_potato.unit_test values ('test', 'animeshbhasin');'''
        self.db_obj.run_sql(update_query, commit_flag=True)
        assert True  # To make sure we reach here

        expected_result = '''[{"id":"test","name":"animeshbhasin"}]'''
        select_query = '''select * from talking_potato.unit_test ;'''
        self.assertEqual(self.db_obj.run_sql(select_query, fetch_flag=True), expected_result)

    def test_insert_row(self):
        """Unit test to test insert_row method

        :return None
        """
        create_data = {
            'id': 'test',
            'name': 'animeshbhasin'
        }
        self.db_obj.insert_row(self.db_schema, self.table_name, create_data)
        assert True  # To make sure we reach here

    def test_get_where_clause_arg(self):
        """Unit test to test get_where_clause_arg method

        :return None
        """
        expected_clause = 'where id={} AND name={}'
        expected_args = ["'test'", "'animeshbhasin'"]
        filter_data = {
            'id': 'test',
            'name': 'animeshbhasin'
        }

        actual_clause, actual_args = self.db_obj.get_where_clause_arg(filter_data)

        self.assertEqual(expected_clause, actual_clause)
        self.assertEqual(expected_args, actual_args)

    def test_get_data(self):
        """Unit test to test get_data method

        :return None
        """
        expected_result = '''[{"id":"test","name":"animeshbhasin"}]'''
        data = {
            'id': 'test',
            'name': 'animeshbhasin'
        }
        self.db_obj.insert_row(self.db_schema, self.table_name, data)
        actual_result = self.db_obj.get_data(self.db_schema, self.table_name, filter_data=data)

        self.assertEqual(expected_result, actual_result)
