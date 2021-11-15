"""
analytics service
"""

import json
import pandas as pd
from db import Database

class Analytics(Database):
    """
    instantiate the analytics service
    """
    def __init__(self, database_url):
        """
        instantiate database object

        :param string database_url: database url to create engine
        """
        Database.__init__(self, database_url=database_url)

    def get_data_df(self, db_schema, table_name, filter_data=None):
        """
        get data by template, and process to dataframe

        :param string db_schema: schema name
        :param string table_name: table name
        :param dictionary filter_data: {column name: column value}
        :return: None
        """
        data = self.get_data(db_schema, table_name, filter_data)
        json_data = json.loads(str(data))
        dataframe = pd.DataFrame(json_data)
        return dataframe

    def group_by_df(self, db_schema, table_name, filter_data=None, col_list=None):
        """
        get data by template, and process to dataframe

        :param string db_schema: schema name
        :param string table_name: table name
        :param dictionary filter_data: {column name: column value}
        :param list col_list: a list of columns in the df to analyze
        :return: None
        """
        dataframe = self.get_data_df(db_schema, table_name, filter_data)
        print(dataframe.groupby(by=col_list).count())

    @staticmethod
    def get_select_clause_cols(filter_data=None):
        """
        create the select clause in sql select statement

        :param dictionary filter_data: {column name: column value}
        :return string clause: the select clause in sql select statement
        """
        if filter_data is None:
            filter_data = {}
        cols = []
        if filter_data == {}:
            clause = ""
        else:
            for col_name in filter_data.keys():
                cols.append(col_name)

            clause = ",".join(cols)

        return clause

    @staticmethod
    def get_user_and_date_between_clause(filter_data=None):
        """
        create where clauses for user_id and time in between

        :param dictionary filter_data: {column name: column value}
            (curently with keys: optional user_id, optional
             thumbtack_business_id, from_date, to_date)
        :return string clause: the where clause
        """
        if filter_data is None:
            return None

        user_clause = None
        user_id = None
        if 'user_id' in filter_data:
            user_id = filter_data['user_id']
            user_clause = 'user_id'
        if 'thumbtack_business_id' in filter_data:
            user_id = filter_data['thumbtack_business_id']
            user_clause = 'thumbtack_business_id'
        from_date = filter_data['from_date']
        to_date = filter_data['to_date']
        clause = "where " + user_clause + "='" + user_id + \
                 "' AND date(contacted_time) between '" \
                 + from_date + "' AND '" + to_date + "' "

        return clause

    def get_grouped_by_date(self, db_schema, table_name,
                            filter_user_date_range=None, filter_data=None):
        """
        rul sql statement that filters based on user_id and time

        :param string db_schema: schema name
        :param string table_name: table name
        :param dictionary filer_user_date_range: user_id and date range
        :param dictionary filter_data: {column_name: column_value}.
            Note: having column_name means add this column to select clause in select statement.
            filter_data keys: required date(contacted_time), optional user_source
        :return list result: the result of the sql select statement
        """
        select_clause = self.get_select_clause_cols(filter_data)
        where_date_clause = ''
        if filter_user_date_range:
            where_date_clause = self.get_user_and_date_between_clause(filter_user_date_range)
        sql_stmt = "select " + select_clause + ",count(*) from " + db_schema + "." + table_name \
                   + " " + where_date_clause + " group by " + select_clause + " order by 1 desc;"
        print(sql_stmt)
        result = self.run_sql(sql_stmt, fetch_flag=True)
        return result
