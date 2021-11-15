"""
unit test for analytics module
"""

import unittest
from analytics import Analytics


class TestTestAnalytics(unittest.TestCase):
    """
    unit test class for analytics.py
    """

    def setUp(self) -> None:
        """Setup analytics unit testing table

        :return None
        """
        self.a_obj = Analytics('postgresql+psycopg2://postgres:postgres@35.238.149.103/tp')

        self.db_schema = 'talking_potato'
        self.table_name = 'analytics_unit_test'

        data = f'''{self.db_schema}.{self.table_name} (user_id varchar, contacted_time timestamp,
        thumbtack_business_id varchar); '''
        create_unit_test_table = 'create table if not exists ' + data

        self.a_obj.engine.execute(create_unit_test_table)

    def tearDown(self):
        """Tear down analytics unit testing table

        :return None
        """
        drop_unit_test_table = f'''drop table {self.db_schema}.{self.table_name};'''
        self.a_obj.engine.execute(drop_unit_test_table)
        self.a_obj = None

    def test_get_select_clause_cols(self):
        """Unit test to test get_select_clause_cols method

        :return None
        """
        expected_clause = 'where user_id={} AND date(contacted_time)={}'
        expected_args = ["'animesh'", "'2021-05-10'"]
        filter_data = {'user_id': 'animesh', 'date(contacted_time)': '2021-05-10'}

        actual_clause, actual_args = self.a_obj.get_where_clause_arg(filter_data)

        self.assertEqual(expected_clause, actual_clause)
        self.assertEqual(expected_args, actual_args)

    def test_get_user_and_date_between_clause(self):
        """Unit test to test get_user_and_date_between_clause method

        :return None
        """
        expected_clause \
    = '''where user_id='animesh' AND date(contacted_time) between '2021-01-01' AND '2021-11-15' '''
        filter_data = {'user_id': 'animesh', 'from_date': '2021-01-01', 'to_date': '2021-11-15'}

        actual_clause = self.a_obj.get_user_and_date_between_clause(filter_data)

        self.assertEqual(expected_clause, actual_clause)

    def test_get_grouped_by_date(self):
        """Unit test to test get_grouped_by_date method

        :return None
        """
        expected_res = '[{"date":"2021-11-15T00:00:00.000Z","count":1},' \
                       '{"date":"2021-11-05T00:00:00.000Z","count":1}]'

        data = [{'user_id': 'animesh', 'contacted_time': '2021-11-05',
                 'thumbtack_business_id': '100'},
                {'user_id': 'animesh', 'contacted_time': '2021-11-15',
                 'thumbtack_business_id': '100'}]
        for row in data:
            self.a_obj.insert_row(self.db_schema, self.table_name, row)

        filter_data = {'date(contacted_time)': 1}
        filter_user_date_range = {'user_id': 'animesh', 'from_date': '2021-01-01',
                                  'to_date': '2021-11-15'}

        actual_result = self.a_obj.get_grouped_by_date(self.db_schema,
                                                       self.table_name,
                                                       filter_user_date_range,
                                                       filter_data)

        self.assertEqual(expected_res, actual_result)
