from sqlalchemy import create_engine


class Database:
    def __init__(self, database_url):
        self.engine = create_engine('postgresql+psycopg2://postgres:postgres@35.238.149.103/tp')

    def get_all_leads(self):
        result = self.engine.execute(
            '''select * from thumbtack.test;'''
        )

        return result

    def insert_row(self, db_schema, table_name, create_data):
        cols = []
        vals = []
        args = []

        for k, v in create_data.items():
            cols.append(k)
            vals.append('{}')
            if type(v) == str:
                args.append("'"+v+"'")
            else:
                args.append(v)

        cols_clause = "(" + ",".join(cols) + ")"
        vals_clause = "values (" + ",".join(vals) + ")"

        sql_stmt = "insert into " + db_schema + "." + table_name + " " + cols_clause + \
                   " " + vals_clause
        sql_stmt = sql_stmt.format(*args)
        self.engine.execute(sql_stmt)