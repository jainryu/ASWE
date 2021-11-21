"""
analytics service
"""

from db import Database
import helper
import ast


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
        :param dictionary filter_user_date_range: user_id and date range
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

    @staticmethod
    def create_dates(from_date, to_date):
        """
        extract or create from date and to date
        """
        if not from_date:
            from_date = '2015-01-01'
        else:
            from_date = from_date.replace("'", "")
            date_format_check = helper.check_date_format(from_date)
            if not date_format_check:
                return None, None
        if not to_date:
            to_date = helper.get_todays_date_str()
        else:
            to_date = to_date.replace("'", "")
            date_format_check = helper.check_date_format(to_date)
            if not date_format_check:
                return None, None
        return from_date, to_date

    def get_message_counts_per_year(self, user, lead_source, dimension, from_year, to_year):
        """
        get a count of messages per year
        """
        yearly_count = {}

        for year in range(from_year, to_year + 1):
            fb_where_dict = {"page_id": user["fb_page_id"],
                             "extract (year from timestamp)": year
                             }
            fb_where_clause, fb_args = self.get_where_clause_arg(fb_where_dict)

            tt_where_dict = {"thumbtack_business_id": user["thumbtack_business_id"],
                             "extract (year from contacted_time)": year
                             }
            tt_where_clause, tt_args = self.get_where_clause_arg(tt_where_dict)

            if lead_source:
                if lead_source == "facebook":
                    if dimension:
                        select_stmt = f"""select {dimension}, count(*) from fb.messages
                                          {fb_where_clause} group by {dimension} 
                                          order by count desc""".format(*fb_args)
                    else:
                        select_stmt = f"select count(*) from fb.messages {fb_where_clause}"
                        select_stmt = select_stmt.format(*fb_args)
                elif lead_source == "thumbtack":
                    if dimension:
                        select_stmt = f"""select {dimension}, count(*) from thumbtack.messages
                                        {tt_where_clause} group by {dimension}
                                        order by count desc""".format(*tt_args)
                    else:
                        select_stmt = f"select count(*) from thumbtack.messages {tt_where_clause}"
                        select_stmt = select_stmt.format(*tt_args)
                result = self.run_sql(select_stmt, fetch_flag=True)
                yearly_count[str(year)] = result[0]["count"]
            else:
                fb_select_stmt = f"select count(*) from fb.messages {fb_where_clause}"
                fb_select_stmt = fb_select_stmt.format(*fb_args)
                tt_select_stmt = f"select count(*) from thumbtack.messages {tt_where_clause}"
                tt_select_stmt = tt_select_stmt.format(*tt_args)
                result1 = self.run_sql(fb_select_stmt, fetch_flag=True)
                result2 = self.run_sql(tt_select_stmt, fetch_flag=True)
                result1 = ast.literal_eval(result1)
                result2 = ast.literal_eval(result2)
                count = result1[0]["count"] + result2[0]["count"]
                print("total count: ", count)
                yearly_count[str(year)] = count
        return yearly_count

    def get_message_counts_per_month_helper(self, user, lead_source, dimension, year, month):
        """
        get message_counts per month helper method
        """
        fb_where_dict = {"page_id": user["fb_page_id"],
                             "extract (year from timestamp)": year,
                             "extract (month from timestamp)": month
                            }
        fb_where_clause, fb_args = self.get_where_clause_arg(fb_where_dict)

        tt_where_dict = {"thumbtack_business_id": user["thumbtack_business_id"],
                            "extract (year from contacted_time)": year,
                            "extract (month from contacted_time)": month
                        }
        tt_where_clause, tt_args = self.get_where_clause_arg(tt_where_dict)

        if lead_source:
            if lead_source == "facebook":
                if dimension:
                    select_stmt = f"""select {dimension}, count(*) from fb.messages
                                      {fb_where_clause} group by {dimension}
                                      order by count desc""".format(*fb_args)
                else:
                    select_stmt = f"select count(*) from fb.messages {fb_where_clause}"
                    select_stmt = select_stmt.format(*fb_args)
            elif lead_source == "thumbtack":
                if dimension:
                    select_stmt = f"""select {dimension}, count(*) from thumbtack.messages
                                    {tt_where_clause} group by {dimension}
                                    order by count desc""".format(*tt_args)
                else:
                    select_stmt = f"select count(*) from thumbtack.messages {tt_where_clause}"
                    select_stmt = select_stmt.format(*tt_args)
            result = self.run_sql(select_stmt, fetch_flag=True)
            return result[0]["count"]
        else:
            select_stmt_ff = f"select count(*) from fb.messages {fb_where_clause}"
            select_stmt_ff = select_stmt_ff.format(*fb_args)
            select_stmt_tt = f"select count(*) from thumbtack.messages {tt_where_clause}"
            select_stmt_tt = select_stmt_tt.format(*tt_args)
            result1 = self.run_sql(select_stmt_ff, fetch_flag=True)
            result2 = self.run_sql(select_stmt_tt, fetch_flag=True)
            result1 = ast.literal_eval(result1)
            result2 = ast.literal_eval(result2)
            count = result1[0]["count"] + result2[0]["count"]
            print("total count: ", count)
            return count

    def get_message_counts_per_month(self, user, lead_source, dimension,
                                     from_year, to_year, from_month, to_month):
        """
        get message counts per month
        """
        print("from year: ",from_year)
        print("from_month: ", from_month)
        print("to year: ",to_year)
        print("to month: ", to_month)
        monthly_count = {}
        if from_year == to_year:
            for month in range(from_month, to_month + 1):
                result = self.get_message_counts_per_month_helper(user,
                                                                  lead_source,
                                                                  dimension,
                                                                  from_year,
                                                                  month)
                monthly_count[f"{str(month)}_{str(from_year)}"] = result
        else:
            for year in range(from_year, to_year + 1):
                print(year)
                if year == from_year:
                    for month in range(from_month, 13):
                        result = self.get_message_counts_per_month_helper(user,
                                                                          lead_source,
                                                                          dimension,
                                                                          year,
                                                                          month)
                        monthly_count[f"{str(month)}_{str(from_year)}"] = result
                elif year == to_year + 1:
                    for month in range(1, to_month +1):
                        result = self.get_message_counts_per_month_helper(user,
                                                                          lead_source,
                                                                          dimension,
                                                                          year,
                                                                          month)
                        monthly_count[f"{str(month)}_{str(from_year)}"] = result
                else:
                    for month in range(1, 13):
                        result = self.get_message_counts_per_month_helper(user,
                                                                          lead_source,
                                                                          dimension,
                                                                          year,
                                                                          month)
                        monthly_count[f"{str(month)}_{str(from_year)}"] = result
        return monthly_count
