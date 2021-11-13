'''
THE MYSQL DATABASE CONNECTION INFO
'''

import os
import pymysql

def get_db_info():
    """
    :return: A dictionary with connect info for MySQL
    """
    db_host = os.environ.get("DBHOST", None)
    db_user = os.environ.get("DBUSER", None)
    db_password = os.environ.get("DBPASSWORD", None)

    if db_host is not None:
        db_info = {
            "host": db_host,
            "user": db_user,
            "password": db_password,
            "cursorclass": pymysql.cursors.DictCursor
        }
    else:
        db_info = {
            "host": "microservice1.ctxt3xtpf1tc.us-east-1.rds.amazonaws.com",
            "user": "admin",
            "password": "cloudcomputing",
            "cursorclass": pymysql.cursors.DictCursor
        }

    return db_info