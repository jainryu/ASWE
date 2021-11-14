import requests
import db
from requests.structures import CaseInsensitiveDict
from base64 import b64encode
from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')
database_url = app.config['DATABASE_URL']

def create_test_data() -> dict:
    url = "https://staging-pro-api.thumbtack.com/v1/test/create-lead"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = "Basic dGh1bWJ0YWNrX3BhcnRuZXI6dGh1bWJ0QGNrIQ=="

    data = "{}"

    resp = requests.post(url, headers=headers, data=data)
    data = resp.json()
    return data 

def thumbtack_send_message(business_id, lead_id, message) -> int:
    database_url = app.config['DATABASE_URL']
    db_obj = db.Database(database_url)
    username = str(db_obj.get_thumbtack_auth(business_id)[0][0])
    password = str(db_obj.get_thumbtack_auth(business_id)[0][1])

    url = "https://staging-pro-api.thumbtack.com/v1/business/{}/lead/{}/message".format(business_id, lead_id)
    # this url is only staging

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    data = '{"text": "{message}"}'
    
    resp = requests.post(url, headers=headers, data=data, auth=(username, password))

    return resp.status_code

def thumbtack_lead_json_to_list(json_dict) -> list:
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

    column_names = ["thumbtack_lead_id", "contacted_time", "price", "thumbtack_request_id", "category", "title", "description", "schedule", "city", "state", "zip", "travel_preferences", "thumbtack_customer_id", "customer_name", "thumbtack_business_id", "thumbtack_business_name"]

    return staging_row, column_names

def thumbtack_message_json_to_list(json_dict) -> list:
    staging_row = []
    for key in json_dict:
        if key == "message":
            staging_row.append(json_dict[key]["messageID"])
            staging_row.append(json_dict[key]["createTimestamp"])
            staging_row.append(json_dict[key]["text"])
        else:
            staging_row.append(json_dict[key])

    column_names = ["thumbtack_lead_id", "thumbtack_customer_id", "thumbtack_business_id", "thumbtack_message_id", "contacted_time", "message_text"]

    return staging_row, column_names


