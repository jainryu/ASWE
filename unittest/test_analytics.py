
import unittest
from server.analytics import Analytics
import pandas as pd
from pandas._testing import assert_frame_equal


analytics = Analytics('database_url')


def test_get_data_df(self):
    analytics.clear_test_table()
    analytics.insert_row('unittest', 'test', {'name': 'test'})
    test_df = pd.DataFrame({'test': '1000'})
    df = analytics.get_data_df('unittest', 'test')
    assert_frame_equal(test_df, df)

    # def group_by_df(self, db_schema, table_name, filter_data=None, col_list=None):
    #     df = self.get_data_df(db_schema, table_name, filter_data)
    #     print(df.groupby(by=col_list).count())
