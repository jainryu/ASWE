"""
thumbtack connection
"""
import requests
from flask import Flask
from requests.structures import CaseInsensitiveDict
import db

app = Flask(__name__)
app.config.from_pyfile('config.py')

def create_test_data() -> dict:
    """
    create thumbtack text data

    :return dict data: thumbtack test data
    """
    url = "https://staging-pro-api.thumbtack.com/v1/test/create-lead"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = "Basic dGh1bWJ0YWNrX3BhcnRuZXI6dGh1bWJ0QGNrIQ=="

    data = "{}"

    resp = requests.post(url, headers=headers, data=data)
    data = resp.json()
    return data

def thumbtack_send_message(business_id, lead_id, message) -> int:
    """
    send message

    :return dict data: thumbtack test data
    """
    database_url = app.config['DATABASE_URL']
    db_obj = db.Database(database_url)
    username = str(db_obj.get_thumbtack_auth(business_id)[0][0])
    password = str(db_obj.get_thumbtack_auth(business_id)[0][1])

    url = f"https://staging-pro-api.thumbtack.com/v1/business/{business_id}/lead/{lead_id}/message"
    # this url is only staging

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    data = {"text": f"{message}"}

    resp = requests.post(url, headers=headers, data=data, auth=(username, password))

    return resp.status_code

def thumbtack_lead_json_to_list(json_dict) -> list:
    """
    format thumbtack lead data from json to list

    :return tuple: tuple containing
        - list staging_row: lead data values
        - list column_names: lead data keys
    """
    staging_row = []
    for key in json_dict:
        if key == "request":
            for request_key in json_dict[key]:
                if request_key == "location":
                    for location_key in json_dict[key][request_key]:
                        staging_row.append(json_dict[key][request_key][location_key])
                else:
                    staging_row.append(json_dict[key][request_key])
        elif key == "customer":
            staging_row.append(json_dict[key]["customerID"])
            staging_row.append(json_dict[key]["name"])
        elif key == "business":
            staging_row.append(json_dict[key]["businessID"])
            staging_row.append(json_dict[key]["name"])
        else:
            staging_row.append(json_dict[key])

    column_names = ["thumbtack_lead_id", "contacted_time", "price",
                    "thumbtack_request_id", "category", "title", "description",
                    "schedule", "city", "state", "zip", "travel_preferences",
                    "thumbtack_customer_id", "customer_name",
                    "thumbtack_business_id", "thumbtack_business_name"]

    return staging_row, column_names

def thumbtack_message_json_to_list(json_dict) -> list:
    """
    format thumbtack message data from json to list

    :return tuple: tuple containing
        - list staging_row: message data values
        - list column_names: lead data keys
    """
    staging_row = []
    for key in json_dict:
        if key == "message":
            staging_row.append(json_dict[key]["messageID"])
            staging_row.append(json_dict[key]["createTimestamp"])
            staging_row.append(json_dict[key]["text"])
        else:
            staging_row.append(json_dict[key])

    column_names = ["thumbtack_lead_id", "thumbtack_customer_id",
                    "thumbtack_business_id", "thumbtack_message_id",
                    "contacted_time", "message_text"]

    return staging_row, column_names
