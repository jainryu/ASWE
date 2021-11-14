from sqlalchemy import create_engine
import pandas as pd

class Database:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)

    def get_all_leads(self):
        result = self.engine.execute(
            '''select * from thumbtack.test;'''
        )

        return result

    def run_sql(self, sql_statement, fetch_flag=False, commit_flag=False):
        connection = None
        res = None
        try:
            connection = self.engine.raw_connection()
            cur = connection.cursor()

            if commit_flag:
                res = cur.execute(sql_statement)
                connection.commit()
            if fetch_flag:
                # col_names = [desc[0] for desc in cur.description]
                # res = cur.fetchall()
                df = pd.read_sql_query(sql_statement, con=self.engine)
                res = df.to_json(orient='records')

            connection.close()
        except Exception as e:
            connection.close()
            raise e

        return res

    def insert_row(self, db_schema, table_name, create_data):
        cols = []
        values = []
        args = []

        for k, v in create_data.items():
            cols.append(k)
            values.append('{}')
            if type(v) == str:
                args.append("'" + v + "'")
            else:
                args.append(v)

        cols_clause = "(" + ",".join(cols) + ")"
        values_clause = "values (" + ",".join(values) + ")"

        sql_stmt = "insert into " + db_schema + "." + table_name + " " + cols_clause + \
                   " " + values_clause
        sql_stmt = sql_stmt.format(*args)
        self.run_sql(sql_stmt, commit_flag=True)


    @staticmethod
    def get_where_clause_arg(filter_data=None):
        if filter_data is None:
            filter_data = {}
        terms = []
        args = []

        if filter_data == {}:
            clause = ""
            args = None
        else:
            for k, v in filter_data.items():
                terms.append(k + "={}")
                if type(v) == str:
                    args.append("'" + v + "'")
                else:
                    args.append(v)

            clause = "where " + " AND ".join(terms)

        return clause, args

    def get_data(self, db_schema, table_name, filter_data=None):
        where_clause, args = self.get_where_clause_arg(filter_data)
        sql_stmt = "select * from " + db_schema + "." + table_name + " " + where_clause

        if args:
            sql_stmt = sql_stmt.format(*args)

        result = self.run_sql(sql_stmt, fetch_flag=True)
        return result


