from db import Database
import pandas as pd
import json


class Analytics(Database):
    def __init__(self, database_url):
        Database.__init__(self, database_url=database_url)

    def get_data_df(self, db_schema, table_name, filter_data=None):
        data = self.get_data(db_schema, table_name, filter_data)
        json_data = json.loads(str(data))
        df = pd.DataFrame(json_data)
        return df

    def group_by_df(self, db_schema, table_name, filter_data=None, col_list=None):
        df = self.get_data_df(db_schema, table_name, filter_data)
        print(df.groupby(by=col_list).count())

    @staticmethod
    def get_select_clause_cols(filter_data=None):
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
        clause = "where " + user_clause + "='" + user_id + "' AND date(contacted_time) between '" + from_date + \
                 "' AND '" + to_date + "' "

        return clause

    def get_grouped_by_date(self, db_schema, table_name, filter_user_date_range=None, filter_data=None):
        select_clause = self.get_select_clause_cols(filter_data)
        where_date_clause = ''
        if filter_user_date_range:
            where_date_clause = self.get_user_and_date_between_clause(filter_user_date_range)
        sql_stmt = "select " + select_clause + ",count(*) from " + db_schema + "." + table_name \
                   + " " + where_date_clause + " group by " + select_clause + " order by 1 desc;"
        print(sql_stmt)
        result = self.run_sql(sql_stmt, fetch_flag=True)
        return result
