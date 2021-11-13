import pymysql

import context


class RDBService:

    def __init__(self):
        pass

    @classmethod
    def _get_db_connection(cls):
        '''
            gets database info from context.py

            :return a pymysql Connection object, which is a socket (ip and port) of a mysql server
                -the connection to the database
        '''

        db_info = context.get_db_info()
        db_connection = pymysql.connect(**db_info, autocommit=True)
        return db_connection

    @classmethod
    def get_by_prefix(cls, db_schema, table_name, column_name, value_prefix):
        '''
            query: select * from {db_schema.table_name} where {column_name} like {value_prefix}

            :param db_schema (string): schema
            :param table_name (string): table_name
            :param column_name (string): column_name
            :return query (as dictionary?)
        '''

        conn = RDBService._get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + db_schema + "." + table_name + " where " + \
            column_name + " like " + "'" + value_prefix + "%'"
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def _get_where_clause_args(cls, template):
        '''
            organizes the template for find_by_template() method

            :param template (dictionary): {column name: column value}
            :return tuple of (string, list):
                -string: " where {key_1}=%s AND {key_2}=%s ... AND {key_n}=%s"
                -list: [{val_1}, ..., {val_n}]
        '''

        terms = []
        args = []
        clause = None

        if template is None or template == {}:
            clause = ""
            args = None
        else:
            for k,v in template.items():
                terms.append(k + "=%s")
                args.append(v)

            clause = " where " +  " AND ".join(terms)


        return clause, args
    
    @classmethod
    def run_sql(cls, sql_statement, args, fetch=False, commit=False):
        '''
            run any sql statement

            :param sql_statement (string): the sql statement
            :param args (list): list of args that matches the '%s' in sql_statement
            :param fetch (bool): if fetching from db
            :return query (as dictionary?)
        '''

        conn = RDBService._get_db_connection()

        try:
            cur = conn.cursor()
            res = cur.execute(sql_statement, args=args)
            if commit:
                conn.commit()
            if fetch:
                res = cur.fetchall()
            conn.close()
        except Exception as e:
            conn.close()
            raise e

        return res

    '''
        :return query
        -with multiple where statements
    '''
    @classmethod
    def find_by_template(cls, db_schema, table_name, template):
        '''
            query with 0 to multiple where clause

            :param db_schema (string): schema
            :param table_name (string): table_name
            :param template (dictionary): where clause in sql
            :return query as list of dictionary
        '''

        wc, args = RDBService._get_where_clause_args(template)
        sql = "select * from " + db_schema + "." + table_name + " " + wc
        res = RDBService.run_sql(sql, args, fetch=True)

        return res
    
    @classmethod
    def delete_by_template(cls, db_schema, table_name, template):
        '''
            delete with 0 to multiple where clause

            :param db_schema (string): schema
            :param table_name (string): table_name
            :param template (dictionary): where clause in sql
            :return query
        '''

        wc, args = RDBService._get_where_clause_args(template)
        sql = "delete from " + db_schema + "." + table_name + " " + wc
        res = RDBService.run_sql(sql, args, commit=True)

        return res


    @classmethod
    def create(cls, db_schema, table_name, create_data):
        '''
            create new record

            :param db_schema (string): schema_name
            :param table_name (string): table_name
            :param create_data (dictionary): {column_name: value}
            :return query
        '''

        cols = []
        vals = []
        args = []

        for k,v in create_data.items():
            cols.append(k)
            vals.append('%s')
            args.append(v)

        cols_clause = "(" + ",".join(cols) + ")"
        vals_clause = "values (" + ",".join(vals) + ")"

        sql_stmt = "insert into " + db_schema + "." + table_name + " " + cols_clause + \
            " " + vals_clause

        res = RDBService.run_sql(sql_stmt, args, commit=True)
        return res

    @classmethod
    def update(cls, db_schema, table_name, update_data, primary_key_col):
        '''
            update record

            :param db_schema (string): schema_name
            :param table_name (string): table_name
            :param create_data (dictionary): {column_name: value}
            :return query
        '''
        primary_key_val = update_data[primary_key_col]

        update_data.pop(primary_key_col)

        updated_cols = []
        updated_args = []
        
        for k,v in update_data.items(): #col1: 1,col2: 2
            updated_cols.append(k + "=%s")
            updated_args.append(v)

        update = ",".join(updated_cols)
        
        sql_stmt =f"update {db_schema}.{table_name} set {update} where {primary_key_col} = {primary_key_val}"
        res = RDBService.run_sql(sql_stmt, updated_args, commit=True)
        return res