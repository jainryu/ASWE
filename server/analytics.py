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
    def get_date_between_clause(filter_data=None):
        if filter_data is None:
            return None

        clause = "where date(contacted_time) between '" + "' AND '".join(filter_data) + "'"

        return clause

    def get_grouped_by_date(self, db_schema, table_name, filter_date_range=None, filter_data=None):
        select_clause = self.get_select_clause_cols(filter_data)
        where_date_clause = ''
        if filter_date_range:
            where_date_clause = self.get_date_between_clause(filter_date_range)
        sql_stmt = "select " + select_clause + ",count(*) from " + db_schema + "." + table_name \
                   + " " + where_date_clause + " group by " + select_clause + " order by 1 desc;"

        result = self.run_sql(sql_stmt, fetch_flag=True)
        return result



# a = Analytics('postgresql+psycopg2://postgres:postgres@35.238.149.103/tp')
# print (a.group_by_df(db_schema = 'talking_potato', table_name = 'messages', col_list=['user_source']))
# x = a.get_grouped_by_date(db_schema='talking_potato', table_name='messages',
#                           filter_date_range=['2021-11-05', '2021-11-13'],
#                           filter_data={'date(contacted_time)': 1, 'user_source': 1})

# x = a.get_grouped_by_date(db_schema='thumbtack', table_name='leads',
#                           filter_date_range=['2021-10-09', '2021-11-15'],
#                           filter_data={'date(contacted_time)': 1})

# x = a.get_grouped_by_date(db_schema='thumbtack', table_name='leads',
#                       filter_data={'date(contacted_time)': '2021-11-05'})
# print(x)

# {'user_source': 'thumbtack', 'date(contacted_time)': '2021-11-05'}
# clause = a.get_select_clause_cols(filter_data={'user_source': 'thumbtack', 'date(contacted_time)': '2021-11-05'})
# print (clause)
