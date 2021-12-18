"""
unit test for analytics module
"""

import unittest
from analytics import Analytics
import helper


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

    def test_create_dates_all_none(self):
        """
        testing create_dates
        """
        from_date = None
        to_date = None
        expected_from = '1900-01-01'
        expected_to = helper.get_todays_date_str()
        actual_from, actual_to = self.a_obj.create_dates("all", from_date, to_date)
        self.assertEqual(expected_from, actual_from)
        self.assertEqual(expected_to, actual_to)

    def test_create_dates_all_both(self):
        """
        testing create_dates
        """
        from_date = "2018-10-10"
        to_date = "2019-11-11"
        expected_from = "2018-10-10"
        expected_to = "2019-11-11"
        actual_from, actual_to = self.a_obj.create_dates("all", from_date, to_date)
        self.assertEqual(expected_from, actual_from)
        self.assertEqual(expected_to, actual_to)
    
    def test_create_dates_all_both_wrong(self):
        """
        testing create_dates wrong format 1
        """
        from_date = "ac"
        to_date = "abc"
        expected_from = None
        expected_to = None
        actual_from, actual_to = self.a_obj.create_dates("all", from_date, to_date)
        self.assertEqual(expected_from, actual_from)
        self.assertEqual(expected_to, actual_to)

    def test_create_dates_years_none(self):
        """
        testing create_dates 3. should work as of 2021
        """
        from_date = None
        to_date = None
        expected_from = "2011"
        expected_to = "2021"
        actual_from, actual_to = self.a_obj.create_dates("years", from_date, to_date)
        self.assertEqual(expected_from, actual_from)
        self.assertEqual(expected_to, actual_to)

    def test_create_dates_years_both(self):
        """
        testing create_dates 4. should work as of 2021
        """
        from_date = "2018"
        to_date = "2019"
        expected_from = "2018"
        expected_to = "2019"
        actual_from, actual_to = self.a_obj.create_dates("years", from_date, to_date)
        self.assertEqual(expected_from, actual_from)
        self.assertEqual(expected_to, actual_to)

    def test_create_dates_years_both_wrong(self):
        """
        testing create_dates wrong format 1
        """
        from_date = "ac"
        to_date = "abc"
        expected_from = None
        expected_to = None
        actual_from, actual_to = self.a_obj.create_dates("years", from_date, to_date)
        self.assertEqual(expected_from, actual_from)
        self.assertEqual(expected_to, actual_to)

    def test_create_dates_months_none(self):
        """
        testing create_dates 5. should work as of 2021-12
        """
        from_date = None
        to_date = None
        expected_from = "2020-12"
        expected_to = "2021-12"
        actual_from, actual_to = self.a_obj.create_dates("months", from_date, to_date)
        self.assertEqual(expected_from, actual_from)
        self.assertEqual(expected_to, actual_to)

    def test_create_dates_months_both(self):
        """
        testing create_dates 5. should work as of 2021-12
        """
        from_date = "2018-1"
        to_date = "2019-12"
        expected_from = "2018-1"
        expected_to = "2019-12"
        actual_from, actual_to = self.a_obj.create_dates("months", from_date, to_date)
        self.assertEqual(expected_from, actual_from)
        self.assertEqual(expected_to, actual_to)
    
    def test_create_dates_months_both_wrong(self):
        """
        testing create_dates wrong format 1
        """
        from_date = "ac"
        to_date = "abc"
        expected_from = None
        expected_to = None
        actual_from, actual_to = self.a_obj.create_dates("months", from_date, to_date)
        self.assertEqual(expected_from, actual_from)
        self.assertEqual(expected_to, actual_to)

    def test_single_source_year_count_aggregator(self):
        """
        test single_source_year_count_aggregator()
        """
        sql_res = [{"year": 2021.0, "count": 2}, {"year": 2017.0, "count": 8}]
        from_year = 2015
        to_year = 2021
        expected_result = {2015: 0, 2016: 0, 2017: 8, 2018: 0, 2019: 0, 2020: 0, 2021: 2}
        actual_result = self.a_obj.single_source_year_count_aggregator(sql_res, from_year, to_year)
        self.assertEqual(expected_result, actual_result)
    
    def test_single_source_month_count_aggregator(self):
        """
        test single_source_month_count_aggregator()
        """
        sql_res = [{"year":2021.0, "month": 1, "count": 2}]
        from_year = 2020
        from_month = 12
        to_year = 2022
        to_month = 2
        expected_result = {'2020_12': 0, '2021_1': 0, '2021_2': 0, '2021_3': 0, '2021_4': 0, '2021_5': 0,
                           '2021_6': 0, '2021_7': 0, '2021_8': 0, '2021_9': 0, '2021_10': 0, '2021_11': 0,
                           '2021_12': 0, '2022_1': 0, '2022_2': 0}
        actual_result = self.a_obj.single_source_month_count_aggregator(sql_res, from_year, to_year, from_month, to_month)
        self.assertEqual(expected_result, actual_result)

    def test_single_source_month_count_aggregator_2(self):
        """
        test single_source_month_count_aggregator()
        """
        sql_res = [{"year":2020.0, "month": 5, "count": 2}]
        from_year = 2020
        from_month = 5
        to_year = 2020
        to_month = 5
        expected_result = {'2020_5': 2}
        actual_result = self.a_obj.single_source_month_count_aggregator(sql_res, from_year, to_year, from_month, to_month)
        self.assertEqual(expected_result, actual_result)

    def test_both_source_year_count_aggregator(self):
        """
        test both_source_year_count_aggregator()
        """
        fb_sql_result = [{"year":2021.0,"count":24}]
        tt_sql_result = [{"year":2021.0,"count":2},{"year":2017.0,"count":8}]
        from_year = 2020
        to_year = 2021
        expected_result = {2020: {'facebook': 0, 'thumbtack': 0, 'total': 0},
                           2021: {'facebook': 24, 'thumbtack': 2, 'total': 26}}
        actual_result = self.a_obj.both_source_year_count_aggregator(fb_sql_result, tt_sql_result, from_year, to_year)
        self.assertEqual(expected_result, actual_result)

    def test_both_source_month_count_aggregator(self):
        """
        test both_source_month_count_aggregator()
        """
        fb_sql_result = [{"year":2021.0, "month": 1, "count":24}]
        tt_sql_result = [{"year":2021.0, "month": 1, "count":2},{"year":2017.0, "month": 1, "count":8}]
        from_year = 2020
        to_year = 2022
        from_month = 12
        to_month = 1
        expected_result = {'2020_12': {'facebook': 0, 'thumbtack': 0, 'total': 0},
                           '2021_1': {'facebook': 0, 'thumbtack': 0, 'total': 0},
                           '2021_2': {'facebook': 0, 'thumbtack': 0, 'total': 0},
                           '2021_3': {'facebook': 0, 'thumbtack': 0, 'total': 0},
                           '2021_4': {'facebook': 0, 'thumbtack': 0, 'total': 0},
                           '2021_5': {'facebook': 0, 'thumbtack': 0, 'total': 0},
                           '2021_6': {'facebook': 0, 'thumbtack': 0, 'total': 0},
                           '2021_7': {'facebook': 0, 'thumbtack': 0, 'total': 0},
                           '2021_8': {'facebook': 0, 'thumbtack': 0, 'total': 0},
                           '2021_9': {'facebook': 0, 'thumbtack': 0, 'total': 0},
                           '2021_10': {'facebook': 0, 'thumbtack': 0, 'total': 0},
                           '2021_11': {'facebook': 0, 'thumbtack': 0, 'total': 0},
                           '2021_12': {'facebook': 0, 'thumbtack': 0, 'total': 0},
                           '2022_1': {'facebook': 0, 'thumbtack': 0, 'total': 0}}
        actual_result = self.a_obj.both_source_month_count_aggregator(fb_sql_result, tt_sql_result, from_year, to_year, from_month, to_month)
        self.assertEqual(expected_result, actual_result)
    
    def test_both_source_month_count_aggregator_2(self):
        """
        test both_source_month_count_aggregator()
        """
        fb_sql_result = [{"year":2021.0, "month": 1, "count":24}]
        tt_sql_result = [{"year":2021.0, "month": 1, "count":2},{"year":2017.0, "month": 1, "count":8}]
        from_year = 2020
        to_year = 2020
        from_month = 1
        to_month = 1
        expected_result = {'2020_1': {'facebook': 0, 'thumbtack': 0, 'total': 0}}
        actual_result = self.a_obj.both_source_month_count_aggregator(fb_sql_result, tt_sql_result, from_year, to_year, from_month, to_month)
        self.assertEqual(expected_result, actual_result)
    
    def test_get_message_counts_per_year_1(self):
        """
        test get_message_counts_per_year()
        facebook, no dimension, no format
        """
        
        user = {'username': 'tojo',
                'thumbtack_business_id': '286845156044809661',
                'fb_page_id': '103603665458708'}
        lead_source = 'facebook'
        dimension = None
        from_year = 2020
        to_year = 2021
        data_format = None
        expected_result = {'facebook': [{'year': 2021.0, 'count': 24}]}
        actual_result = self.a_obj.get_message_counts_per_year(user, lead_source, dimension, from_year, to_year, data_format)
        self.assertEqual(expected_result, actual_result)
    
    def test_get_message_counts_per_year_2(self):
        """
        test get_message_counts_per_year()
        facebook, dimension, no format
        """
        
        user = {'username': 'tojo',
                'thumbtack_business_id': '286845156044809661',
                'fb_page_id': '103603665458708'}
        lead_source = 'facebook'
        dimension = 'recipient_id'
        from_year = 2020
        to_year = 2021
        data_format = None
        expected_result = {'facebook': [{'year': 2021.0, 'recipient_id': '103603665458708', 'count': 24}]}
        actual_result = self.a_obj.get_message_counts_per_year(user, lead_source, dimension, from_year, to_year, data_format)
        self.assertEqual(expected_result, actual_result)
    
    def test_get_message_counts_per_year_3(self):
        """
        test get_message_counts_per_year()
        thumbtack, no dimension, no format
        """
        
        user = {'username': 'tojo',
                'thumbtack_business_id': '286845156044809661',
                'fb_page_id': '103603665458708'}
        lead_source = 'thumbtack'
        dimension = None
        from_year = 2020
        to_year = 2021
        data_format = None
        expected_result = {'thumbtack': [{'year': 2021.0, 'count': 2}]}
        actual_result = self.a_obj.get_message_counts_per_year(user, lead_source, dimension, from_year, to_year, data_format)
        self.assertEqual(expected_result, actual_result)

    def test_get_message_counts_per_year_4(self):
        """
        test get_message_counts_per_year()
        thumbtack, dimension, no format
        """
        
        user = {'username': 'tojo',
                'thumbtack_business_id': '286845156044809661',
                'fb_page_id': '103603665458708'}
        lead_source = 'thumbtack'
        dimension = 'message_text'
        from_year = 2020
        to_year = 2021
        data_format = None
        expected_result = {'thumbtack': [{'year': 2021.0, 'message_text': 'Do you offer fridge cleaning or is that extra?', 'count': 1}, {'year': 2021.0, 'message_text': 'Hi how are you?', 'count': 1}]}
        actual_result = self.a_obj.get_message_counts_per_year(user, lead_source, dimension, from_year, to_year, data_format)
        self.assertEqual(expected_result, actual_result)
    
    def test_get_message_counts_per_year_5(self):
        """
        test get_message_counts_per_year()
        thumbtack, dimension, format
        """
        
        user = {'username': 'tojo',
                'thumbtack_business_id': '286845156044809661',
                'fb_page_id': '103603665458708'}
        lead_source = 'thumbtack'
        dimension = 'message_text'
        from_year = 2020
        to_year = 2021
        data_format = 'by_year'
        expected_result = {2020: 0, 2021: 1}
        actual_result = self.a_obj.get_message_counts_per_year(user, lead_source, dimension, from_year, to_year, data_format)
        self.assertEqual(expected_result, actual_result)
    
    def test_get_message_counts_per_year_6(self):
        """
        test get_message_counts_per_year()
        no source, no dimension, no format
        """
        user = {'username': 'tojo',
                'thumbtack_business_id': '286845156044809661',
                'fb_page_id': '103603665458708'}
        lead_source = None
        dimension = None
        from_year = 2020
        to_year = 2021
        data_format = None
        expected_result = {'facebook': [{'year': 2021.0, 'count': 24}], 'thumbtack': [{'year': 2021.0, 'count': 2}]}
        actual_result = self.a_obj.get_message_counts_per_year(user, lead_source, dimension, from_year, to_year, data_format)
        self.assertEqual(expected_result, actual_result)
    
    def test_get_message_counts_per_year_7(self):
        """
        test get_message_counts_per_year()
        no source, no dimension, format
        """
        user = {'username': 'tojo',
                'thumbtack_business_id': '286845156044809661',
                'fb_page_id': '103603665458708'}
        lead_source = None
        dimension = None
        from_year = 2020
        to_year = 2021
        data_format = "by_year"
        expected_result = {2020: {'facebook': 0, 'thumbtack': 0, 'total': 0}, 2021: {'facebook': 24, 'thumbtack': 2, 'total': 26}}
        actual_result = self.a_obj.get_message_counts_per_year(user, lead_source, dimension, from_year, to_year, data_format)
        self.assertEqual(expected_result, actual_result)

    def test_get_message_counts_per_month_1(self):
        """
        test get_message_counts_per_month()
        facebook, no dimension, no format
        """
        
        user = {'username': 'tojo',
                'thumbtack_business_id': '286845156044809661',
                'fb_page_id': '103603665458708'}
        lead_source = 'facebook'
        dimension = None
        from_year = 2020
        to_year = 2021
        from_month = 1
        to_month = 12
        data_format = None
        expected_result = {'facebook': [{'year': 2021.0, 'month': 11.0, 'count': 24}]}
        actual_result = self.a_obj.get_message_counts_per_month(user, lead_source, dimension,\
                                     from_year, to_year, from_month, to_month, data_format)
        self.assertEqual(expected_result, actual_result)
    
    def test_get_message_counts_per_month_2(self):
        """
        test get_message_counts_per_month()
        facebook, dimension, no format
        """
        
        user = {'username': 'tojo',
                'thumbtack_business_id': '286845156044809661',
                'fb_page_id': '103603665458708'}
        lead_source = 'facebook'
        dimension = 'recipient_id'
        from_year = 2020
        to_year = 2021
        from_month = 1
        to_month = 12
        data_format = None
        expected_result = {'facebook': [{'year': 2021.0, 'month': 11.0, 'recipient_id': '103603665458708', 'count': 24}]}
        actual_result = self.a_obj.get_message_counts_per_month(user, lead_source, dimension,\
                                     from_year, to_year, from_month, to_month, data_format)
        self.assertEqual(expected_result, actual_result)
    
    def test_get_message_counts_per_month_3(self):
        """
        test get_message_counts_per_month()
        thumbtack, no dimension, no format
        """
        
        user = {'username': 'tojo',
                'thumbtack_business_id': '286845156044809661',
                'fb_page_id': '103603665458708'}
        lead_source = 'thumbtack'
        dimension = None
        from_year = 2020
        to_year = 2021
        from_month = 1
        to_month = 12
        data_format = None
        expected_result = {'thumbtack': [{'year': 2021.0, 'month': 10.0, 'count': 1}, {'year': 2021.0, 'month': 11.0, 'count': 1}]}
        actual_result = self.a_obj.get_message_counts_per_month(user, lead_source, dimension,\
                                     from_year, to_year, from_month, to_month, data_format)
        self.assertEqual(expected_result, actual_result)
    
    def test_get_message_counts_per_month_4(self):
        """
        test get_message_counts_per_month()
        thumbtack, dimension, no format
        """
        
        user = {'username': 'tojo',
                'thumbtack_business_id': '286845156044809661',
                'fb_page_id': '103603665458708'}
        lead_source = 'thumbtack'
        dimension = "message_text"
        from_year = 2020
        to_year = 2021
        from_month = 1
        to_month = 12
        data_format = None
        expected_result = {'thumbtack': [{'year': 2021.0, 'month': 10.0, 'message_text': 'Do you offer fridge cleaning or is that extra?', 'count': 1}, 
                                         {'year': 2021.0, 'month': 11.0, 'message_text': 'Hi how are you?', 'count': 1}]}
        actual_result = self.a_obj.get_message_counts_per_month(user, lead_source, dimension,\
                                     from_year, to_year, from_month, to_month, data_format)
        self.assertEqual(expected_result, actual_result)

    def test_get_message_counts_per_month_5(self):
        """
        test get_message_counts_per_month()
        thumbtack, dimension, format
        """
        
        user = {'username': 'tojo',
                'thumbtack_business_id': '286845156044809661',
                'fb_page_id': '103603665458708'}
        lead_source = 'thumbtack'
        dimension = "message_text"
        from_year = 2021
        to_year = 2021
        from_month = 9
        to_month = 12
        data_format = 'by_year'
        expected_result = {'2021_9': 0, '2021_10': 1, '2021_11': 1, '2021_12': 0}
        actual_result = self.a_obj.get_message_counts_per_month(user, lead_source, dimension,\
                                     from_year, to_year, from_month, to_month, data_format)
        self.assertEqual(expected_result, actual_result)
    
    def test_get_message_counts_per_month_6(self):
        """
        test get_message_counts_per_month()
        """
        
        user = {'username': 'tojo',
                'thumbtack_business_id': '286845156044809661',
                'fb_page_id': '103603665458708'}
        lead_source = None
        dimension = None
        from_year = 2020
        to_year = 2021
        from_month = 1
        to_month = 12
        data_format = None
        expected_result = {'facebook': [{'year': 2021.0, 'month': 11.0, 'count': 24}], 
                           'thumbtack': [{'year': 2021.0, 'month': 10.0, 'count': 1}, {'year': 2021.0, 'month': 11.0, 'count': 1}]}
        actual_result = self.a_obj.get_message_counts_per_month(user, lead_source, dimension,\
                                     from_year, to_year, from_month, to_month, data_format)
        self.assertEqual(expected_result, actual_result)
    
    def test_get_message_counts_per_month_7(self):
        """
        test get_message_counts_per_month()
        """
        
        user = {'username': 'tojo',
                'thumbtack_business_id': '286845156044809661',
                'fb_page_id': '103603665458708'}
        lead_source = None
        dimension = None
        from_year = 2021
        to_year = 2021
        from_month = 9
        to_month = 12
        data_format = 'by_year'
        expected_result = {'2021_9': {'facebook': 0, 'thumbtack': 0, 'total': 0},
                           '2021_10': {'facebook': 0, 'thumbtack': 1, 'total': 1},
                           '2021_11': {'facebook': 24, 'thumbtack': 1, 'total': 25},
                           '2021_12': {'facebook': 0, 'thumbtack': 0, 'total': 0}}
        actual_result = self.a_obj.get_message_counts_per_month(user, lead_source, dimension,\
                                     from_year, to_year, from_month, to_month, data_format)
        self.assertEqual(expected_result, actual_result)