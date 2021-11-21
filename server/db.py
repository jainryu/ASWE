"""
database service
"""

import datetime
from sqlalchemy import create_engine
import pandas as pd


class Database:
    """
    instantiate the database service
    contains sql commands
    """
    engine = None

    def __init__(self, database_url):
        """
        creates sql engine
        :param string database_url: database url to create engine
        """
        self.engine = create_engine(database_url)

    def get_thumbtack_auth(self, business_id):
        """
        get thumbtack authentication

        :param string business_id: talking_potato.users.business_id
        :return list result: result of sql query
        """
        if business_id[0] != "\"":
            business_id = "'" + business_id + "'"
        result = self.engine.execute(f"""select thumbtack_user_id, thumbtack_password
                from talking_potato.users
                where thumbtack_business_id = {business_id}"""
                                     ).fetchall()

        return result

    def run_sql(self, sql_statement, fetch_flag=False, commit_flag=False):
        """
        run any sql statement

        :param string sql_statement: the sql statement
        :param bool fetch_flag: if fetching from db
        :param bool commit_flag: whether to commit to sql server
        :return list res: query
        """
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
                dataframe = pd.read_sql_query(sql_statement, con=self.engine)
                res = dataframe.to_json(orient='records', date_format='iso')

            connection.close()
        except Exception as exception:
            connection.close()
            raise exception

        return res

    def insert_row(self, db_schema, table_name, create_data):
        """
        create new record

        :param string db_schema: schema name
        :param string table_name: table name
        :param dictionary create_data: {column_name: value}
        :return: None
        """
        cols = []
        values = []
        args = []

        for key, val in create_data.items():
            cols.append(key)
            values.append('{}')
            if isinstance(val, str):
                args.append("'" + val + "'")
            else:
                args.append(val)

        cols_clause = "(" + ",".join(cols) + ")"
        values_clause = "values (" + ",".join(values) + ")"

        sql_stmt = "insert into " + db_schema + "." + table_name + " " + cols_clause + \
                   " " + values_clause
        sql_stmt = sql_stmt.format(*args)
        self.engine.execute(sql_stmt)

    def insert_row_from_lead_list(self, db_schema, table_name, data_list, columns):
        """
        insert row from thumbtack lead list

        :param string db_schema: schema name
        :param string table_name: table name
        :param list data_list: the thumbtack lead data
        :param list columns: column names that correspond to the data_list values
        :return: None
        """
        data_list_len = len(data_list)
        for i in range(data_list_len):
            data_list[i] = data_list[i].replace('\'', '\'\'')
            if i == 1:
                data_list[i] = datetime.datetime.fromtimestamp(
                    int(data_list[i])).strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(data_list[i], str):
                data_list[i] = "'" + data_list[i] + "'"

        values_clause = "values (" + ",".join(data_list) + ")"
        cols_clause = "(" + ",".join(columns) + ")"

        sql_stmt = "insert into " + db_schema + "." + table_name + " " + cols_clause + \
                   " " + values_clause
        self.engine.execute(sql_stmt)

    def insert_row_from_message_list(self, db_schema, table_name, data_list, columns):
        """
        insert row from thumbtack messsage list

        :param string db_schema: schema name
        :param string table_name: table name
        :param list data_list: the thumbtack message data
        :param list columns: column names that correspond to the data_list values
        :return: None
        """
        len_data_list = len(data_list)
        for i in range(len_data_list):
            data_list[i] = data_list[i].replace('\'', '\'\'')
            if i == 4:
                data_list[i] = datetime.datetime.fromtimestamp(
                    int(data_list[i])).strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(data_list[i], str):
                data_list[i] = "'" + data_list[i] + "'"

        values_clause = "values (" + ",".join(data_list) + ")"
        cols_clause = "(" + ",".join(columns) + ")"

        sql_stmt = "insert into " + db_schema + "." + table_name + " " + cols_clause + \
                   " " + values_clause
        self.engine.execute(sql_stmt)

    @staticmethod
    def get_where_clause_arg(filter_data=None):
        """
         formats the 'get where' clause in an sql statement

            :param dictionary filter_data: {column name: column value}
            :return tuple: a tuple containing
                -string clause: " where {key_1}=%s AND {key_2}=%s ... AND {key_n}=%s"
                -list args: [{val_1}, ..., {val_n}]
        """
        if filter_data is None:
            filter_data = {}
        terms = []
        args = []

        if filter_data == {}:
            clause = ""
            args = None
        else:
            for key, val in filter_data.items():
                terms.append(key + "={}")
                if isinstance(val, str):
                    args.append("'" + val + "'")
                else:
                    args.append(val)

            clause = "where " + " AND ".join(terms)

        return clause, args

    def get_data(self, db_schema, table_name, filter_data=None):
        """
        select statement with 0 to multiple where clause

        :param string db_schema: schema
        :param string table_name: table name
        :param filter_data: where clause in sql
        :return list result: result of sql select statement
        """
        where_clause, args = self.get_where_clause_arg(filter_data)
        sql_stmt = "select * from " + db_schema + "." + table_name + " " + where_clause

        if args:
            sql_stmt = sql_stmt.format(*args)

        result = self.run_sql(sql_stmt, fetch_flag=True)
        return result

    def update(self, db_schema, table_name, update_data, where_filter):
        '''
            update record

            :param string db_schema: schema
            :param string table_name: table name
            :param dictionary update_data: {column_name: value}
            :return query
        '''
        where_filter_val = update_data[where_filter]
        update_data.pop(where_filter)

        updated_cols = []
        updated_args = []

        for key, val in update_data.items():
            updated_cols.append(key + "={}")
            if isinstance(val, str):
                updated_args.append("'" + val + "'")
            else:
                updated_args.append(val)

        update = ",".join(updated_cols)

        sql_stmt =f"""update {db_schema}.{table_name}
                      set {update}
                      where {where_filter} = '{where_filter_val}'"""
        sql_stmt = sql_stmt.format(*updated_args)
        self.engine.execute(sql_stmt)

    def delete_by_template(self, db_schema, table_name, template):
        '''
            delete with 0 to multiple where clause

            :param string db_schema: schema
            :param string table_name: table_name
            :param dictionary template: where clause in sql
            :return query
        '''

        where_clause, args = self.get_where_clause_arg(template)
        sql_stmt = f"delete from {db_schema}.{table_name} {where_clause}"
        sql_stmt = sql_stmt.format(*args)
        self.engine.execute(sql_stmt)
