"""
analytics service
"""

import ast

from db import Database
import helper
import visualizer

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
        result = self.run_sql(sql_stmt, fetch_flag=True)
        return result

    @staticmethod
    def create_dates(from_date, to_date):
        """
        extract or create from_date and to_date for analytics

        :param string/None from_date: from date
        :param string/None to_date: to date
        :return tuple: a tuple containing
            string from_date: from date
            string to_date: to date
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

    def single_source_year_count_aggregator(self, sql_result, from_year, to_year):
        '''
        reformat sql to show a count vs year relationship

        :param list of dict sql_result: e.g. [{"year": 2021.0, count": 2},
                                              {"year": 2017.0, "count": 8}]
        :param int from_year: from year
        :param int to_year: to year

        :return dict final: e.g. {2021: 2, 2017: 8}
        '''
        final = {}
        for year in range(from_year, to_year + 1):
            final[year] = 0
        for year_counts in sql_result:
            year = int(year_counts["year"])
            count = year_counts["count"]
            if year >= from_year and year <= to_year:
                final[year] = count
        return final

    def single_source_month_count_aggregator(self, sql_result,
                                             from_year, to_year,
                                             from_month, to_month):
        '''
        reformat sql to show a count vs year_month relationship

        :param list of dict sql_result: e.g. [{"year":2021.0, "month": 0, "count": 2}]
        :param int from_year: from year
        :param int to_year: to year

        :return dict final: e.g. {2021_0: 2, 2017_1: 8}
        '''

        final = {}
        for year in range(from_year, to_year + 1):
            if from_year == to_year:
                for month in range(from_month, to_month + 1):
                    final[f"{str(year)}_{str(month)}"] = 0
            elif year == from_year:
                for month in range(from_month, 13):
                    final[f"{str(year)}_{str(month)}"] = 0
            elif year == to_year:
                for month in range(1, to_month + 1):
                    final[f"{str(year)}_{str(month)}"] = 0
            else:
                for month in range(1,13):
                    final[f"{str(year)}_{str(month)}"] = 0
        for year_month_counts in sql_result:
            year = int(year_month_counts["year"])
            month = int(year_month_counts["month"])
            count = year_month_counts["count"]
            if from_year == to_year:
                if (year == from_year) and (month >= from_month) and (month <= to_month):
                    final[f"{str(year)}_{str(month)}"] = count
            else:
                if (year == from_year) and (month >= from_month):
                    final[f"{str(year)}_{str(month)}"] = count
                elif (year == to_year) and (month <= to_month):
                    final[f"{str(year)}_{str(month)}"] = count

        return final

    def both_source_year_count_aggregator(self, fb_sql_result, tt_sql_result, from_year, to_year):
        '''
        reformat sql to show a (fb count, tt count, and total count) vs year relationship

        :param list of dict fb_sql_result: e.g. [{"year":2021.0,"count":24}]
        :param list of dict tt_sql_result: e.g.[{"year":2021.0,"count":2},{"year":2017.0,"count":8}]
        :param int from_year: from year
        :param int to_year: to year

        :return dict final: e.g. {2021: {facebook: 24, thumbtack: 2, total: 26}}
        '''

        final = {}
        for year in range(from_year, to_year + 1):
            final[year] = 0
        for year_counts in fb_sql_result:
            year = int(year_counts["year"])
            count = year_counts["count"]
            if year >= from_year and year <= to_year:
                final[year] = {"facebook": count, "thumbtack": 0, "total": count}
        for year_counts in tt_sql_result:
            year = int(year_counts["year"])
            count = year_counts["count"]
            if year >= from_year and year <= to_year:
                if year in final:
                    final[year]["thumbtack"] = count
                    final[year]["total"] = final[year]["total"] + count
                else:
                    final[year] = {"facebook": 0, "thumbtack": count, "total": count}
        return final

    def both_source_month_count_aggregator(self, fb_sql_result, tt_sql_result,
                                           from_year, to_year, from_month, to_month):
        '''
        reformat sql to show a (fb count, tt count, and total count) vs year_month relationship

        :param list of dict fb_sql_result: e.g. [{"year":2021.0", "month": 0, count":24}]
        :param list of dict tt_sql_result: e.g.[{"year":2021.0,"count":2},{"year":2017.0,"count":8}]
        :param int from_year: from year
        :param int to_year: to year

        :return dict final: e.g. {2021: {facebook: 24, thumbtack: 2, total: 26}}
        '''

        final = {}
        for year in range(from_year, to_year + 1):
            if from_year == to_year:
                for month in range(from_month, to_month + 1):
                    final[f"{str(year)}_{str(month)}"] = {"facebook": 0, "thumbtack": 0, "total": 0}
            elif year == from_year:
                for month in range(from_month, 13):
                    final[f"{str(year)}_{str(month)}"] = {"facebook": 0, "thumbtack": 0, "total": 0}
            elif year == to_year:
                for month in range(1, to_month + 1):
                    final[f"{str(year)}_{str(month)}"] = {"facebook": 0, "thumbtack": 0, "total": 0}
            else:
                for month in range(1,13):
                    final[f"{str(year)}_{str(month)}"] = {"facebook": 0, "thumbtack": 0, "total": 0}
        for year_month_counts in fb_sql_result:
            year = int(year_month_counts["year"])
            month = int(year_month_counts["month"])
            count = year_month_counts["count"]

            if from_year == to_year:
                if (year == from_year) and (month >= from_month) and (month <= to_month):
                    final[f"{str(year)}_{str(month)}"] = {"facebook": count,
                                                          "thumbtack": 0,
                                                          "total": count}
            else:
                if (year == from_year) and (month >= from_month):
                    final[f"{str(year)}_{str(month)}"] = {"facebook": count,
                                                          "thumbtack": 0,
                                                          "total": count}
                elif (year == to_year) and (month <= to_month):
                    final[f"{str(year)}_{str(month)}"] = {"facebook": count,
                                                          "thumbtack": 0,
                                                          "total": count}
        for year_month_counts in tt_sql_result:
            year = int(year_month_counts["year"])
            month = int(year_month_counts["month"])
            count = year_month_counts["count"]

            if from_year == to_year:
                if (year == from_year) and (month >= from_month) and (month <= to_month):
                    if f"{str(year)}_{str(month)}" in final:
                        final[f"{str(year)}_{str(month)}"]["thumbtack"] = count
                        final[f"{str(year)}_{str(month)}"]["total"] = \
                            final[f"{str(year)}_{str(month)}"]["total"] + count
                    else:
                        final[f"{str(year)}_{str(month)}"] = {"facebook": 0,
                                                              "thumbtack": count,
                                                              "total": count}
            else:
                if (year == from_year) and (month >= from_month):
                    if f"{str(year)}_{str(month)}" in final:
                        final[f"{str(year)}_{str(month)}"]["thumbtack"] = count
                        final[f"{str(year)}_{str(month)}"]["total"] = \
                            final[f"{str(year)}_{str(month)}"]["total"] + count
                    else:
                        final[f"{str(year)}_{str(month)}"] = {"facebook": 0,
                                                                "thumbtack": count,
                                                                "total": count}
                elif (year == to_year) and (month <= to_month):
                    if f"{str(year)}_{str(month)}" in final:
                        final[f"{str(year)}_{str(month)}"]["thumbtack"] = count
                        final[f"{str(year)}_{str(month)}"]["total"] = \
                            final[f"{str(year)}_{str(month)}"]["total"] + count
                    else:
                        final[f"{str(year)}_{str(month)}"] = {"facebook": 0,
                                                                "thumbtack": count,
                                                                "total": count}

        return final

    def get_message_counts_per_year(self, user, lead_source, dimension, from_year, to_year, graph):
        """
        get a count of messages per year

        :param dict user: user credentials
        :param string lead_source: an optional lead source specifier
        :param string dimension: optional dimensions to group counts by (along with year)
        :param string from_year: starting year to get message counts
        :param string to_year: ending year to get message counts
        :param string graph: (optional) reformat return for easy graphing
        :return dict:
            if graph is None: e.g. {"facebook": [{"count": 24, "year": 2021}],
                                    "thumbtack" [{"count": 24, "year": 2021}]}
            else: e.g. {"2021": {"facebook": 24, "thumbtack": 2, "total": 26}}
        """
        fb_where_dict = {"page_id": user["fb_page_id"]}
        fb_where_clause, fb_args = self.get_where_clause_arg(fb_where_dict)

        tt_where_dict = {"thumbtack_business_id": user["thumbtack_business_id"]}
        tt_where_clause, tt_args = self.get_where_clause_arg(tt_where_dict)

        fb_select_and_group_by_clause = "extract (year from timestamp)"
        tt_select_and_group_by_clause = "extract (year from contacted_time)"

        if lead_source:
            if lead_source == "facebook":
                if dimension:
                    select_stmt = f"""select {fb_select_and_group_by_clause} as year,
                                        {dimension}, count(*)
                                      from fb.messages {fb_where_clause}
                                      group by {fb_select_and_group_by_clause}, {dimension}
                                      order by year asc""".format(*fb_args)
                else:
                    select_stmt = f"""select {fb_select_and_group_by_clause} as year, count(*)
                                      from fb.messages {fb_where_clause}
                                      group by {fb_select_and_group_by_clause}
                                      order by year asc""".format(*fb_args)
            elif lead_source == "thumbtack":
                if dimension:
                    select_stmt = f"""select {tt_select_and_group_by_clause} as year,
                                        {dimension}, count(*)
                                      from thumbtack.messages {tt_where_clause}
                                      group by {tt_select_and_group_by_clause}, {dimension}
                                      order by year asc""".format(*tt_args)
                else:
                    select_stmt = f"""select {tt_select_and_group_by_clause} as year, count(*)
                                      from thumbtack.messages {tt_where_clause}
                                      group by {tt_select_and_group_by_clause}
                                      order by year asc""".format(*tt_args)
            result = self.run_sql(select_stmt, fetch_flag=True)
            result = ast.literal_eval(result)
            if graph:
                result = self.single_source_year_count_aggregator(result, from_year, to_year)
                if graph == 'html':
                    title = f"Message Counts Per Month for {lead_source}"
                    x_label = "Month"
                    y_label = "Counts"
                    return visualizer.single_plot(result, title=title, x_label=x_label, y_label=y_label)
                elif graph == 'data':
                    return result
            else:
                result = {f"{lead_source}": result}
                return result

        else:
            fb_select_stmt = f"""select {fb_select_and_group_by_clause} as year, count(*)
                                 from fb.messages {fb_where_clause}
                                 group by {fb_select_and_group_by_clause}
                                 order by year asc""".format(*fb_args)
            tt_select_stmt = f"""select {tt_select_and_group_by_clause} as year, count(*)
                                 from thumbtack.messages {tt_where_clause}
                                 group by {tt_select_and_group_by_clause}
                                 order by year asc""".format(*tt_args)
            fb_result = self.run_sql(fb_select_stmt, fetch_flag=True)
            tt_result = self.run_sql(tt_select_stmt, fetch_flag=True)
            fb_result = ast.literal_eval(fb_result)
            tt_result = ast.literal_eval(tt_result)
            if graph:
                result = self.both_source_year_count_aggregator(fb_result, tt_result,
                                                                from_year, to_year)
                if graph == 'html':
                    title = "Message Counts Per Month"
                    x_label = "Month"
                    y_label = "Counts"
                    return visualizer.both_plot(result, title=title,
                                                x_label=x_label, y_label=y_label)
                elif graph == 'data':
                    return result
            else:
                return {"facebook": fb_result, "thumbtack": tt_result}

    def get_message_counts_per_month(self, user, lead_source, dimension,
                                     from_year, to_year, from_month, to_month, graph):
        """
        get message counts per month

        get a count of messages per year

        :param dict user: user credentials
        :param string lead_source: an optional lead source specifier
        :param string dimension: optional dimensions to group counts by (along with year)
        :param string from_year: starting year to get message counts
        :param string to_year: ending year to get message counts
        :param string graph: (optional) reformat return for easy graphing
        :return dict:
            if graph is None: e.g. {"facebook": [{"count": 24, "month": 11, "year": 2021}, ...],
                                    "thumbtack" [{"count": 2, "month": 11, "year": 2021}, ...]}
            else: e.g. {"2021_11": {"facebook": 24, "thumbtack": 2, "total": 26}, ...}
        """
        fb_where_dict = {"page_id": user["fb_page_id"]}
        fb_where_clause, fb_args = self.get_where_clause_arg(fb_where_dict)

        tt_where_dict = {"thumbtack_business_id": user["thumbtack_business_id"]}
        tt_where_clause, tt_args = self.get_where_clause_arg(tt_where_dict)

        if lead_source:
            if lead_source == "facebook":
                if dimension:
                    select_stmt = f"""select extract (year from timestamp) as year,
                                          extract (month from timestamp) as month, {dimension}, count(*)
                                      from fb.messages {fb_where_clause}
                                      group by extract (year from timestamp), 
                                          extract (month from timestamp), {dimension}
                                      order by year asc, month asc""".format(*fb_args)
                else:
                    select_stmt = f"""select extract (year from timestamp) as year,
                                        extract (month from timestamp) as month, count(*)
                                        from fb.messages {fb_where_clause}
                                        group by extract (year from timestamp),
                                            extract (month from timestamp)
                                        order by year asc, month asc""".format(*fb_args)
            elif lead_source == "thumbtack":
                if dimension:
                    select_stmt = f"""select extract (year from contacted_time) as year,
                                          extract (month from contacted_time) as month, {dimension}, count(*)
                                      from thumbtack.messages {tt_where_clause}
                                      group by extract (year from contacted_time),
                                          extract (month from contacted_time), {dimension}
                                      order by year asc, month asc""".format(*tt_args)
                else:
                    select_stmt = f"""select extract (year from contacted_time) as year,
                                          extract (month from contacted_time) as month, count(*)
                                      from thumbtack.messages {tt_where_clause}
                                      group by extract (year from contacted_time),
                                          extract (month from contacted_time)
                                      order by year asc, month asc""".format(*tt_args)
            result = self.run_sql(select_stmt, fetch_flag=True)
            result = ast.literal_eval(result)
            if graph:
                result = self.single_source_month_count_aggregator(result,
                                                                   from_year, to_year,
                                                                   from_month, to_month)
                if graph == 'html':
                    title = "Message Counts Per Month for {lead_source}"
                    x_label = "Month"
                    y_label = "Counts"
                    return visualizer.single_plot(result, title=title,
                                                  x_label=x_label, y_label=y_label)
                elif graph == 'data':
                    return result
            else:
                result = {f"{lead_source}": result}
                return result

        else:
            fb_select_stmt = f"""select extract (year from timestamp) as year,
                                     extract (month from timestamp) as month, count(*)
                                 from fb.messages {fb_where_clause}
                                 group by extract (year from timestamp),
                                     extract (month from timestamp)
                                 order by year asc, month asc""".format(*fb_args)
            tt_select_stmt = f"""select extract (year from contacted_time) as year,
                                     extract (month from contacted_time) as month, count(*)
                                 from thumbtack.messages {tt_where_clause}
                                 group by extract (year from contacted_time),
                                     extract (month from contacted_time) 
                                 order by year asc, month asc""".format(*tt_args)
            fb_result = self.run_sql(fb_select_stmt, fetch_flag=True)
            tt_result = self.run_sql(tt_select_stmt, fetch_flag=True)
            fb_result = ast.literal_eval(fb_result)
            tt_result = ast.literal_eval(tt_result)
            if graph:
                result = self.both_source_month_count_aggregator(fb_result, tt_result,
                                                                 from_year, to_year,
                                                                 from_month, to_month)
                if graph == 'html':
                    title = "Message Counts Per Month"
                    x_label = "Month"
                    y_label = "Counts"
                    return visualizer.both_plot(result, title=title,
                                                x_label=x_label, y_label=y_label)
                elif graph == 'data':
                    return result
            else:
                return {"facebook": fb_result, "thumbtack": tt_result}
