import requests
from requests.structures import CaseInsensitiveDict
import pandas as pd

def create_test_data() -> dict:
    url = "https://staging-pro-api.thumbtack.com/v1/test/create-lead"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = "Basic dGh1bWJ0YWNrX3BhcnRuZXI6dGh1bWJ0QGNrIQ=="

    data = "{}"

    resp = requests.post(url, headers=headers, data=data)
    data = resp.json()
    return data 

def thumbtack_json_to_pandas(json_dict) -> pd.DataFrame:
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

    print(staging_row)

    return pd.DataFrame([staging_row])




if __name__ == "__main__":
    test_dict = {
    "leadID": "437282430869512192",
    "createTimestamp": "1636428031",
    "price": "More information needed to give an estimate",
    "request": {
        "requestID": "437282427823792129",
        "category": "House Cleaning",
        "title": "House Cleaning",
        "description": "I am looking for someone to clean my apartment before I move",
        "schedule": "Date: Tue, May 05 2020\nTime: 6:00 PM\nLength: 3.5 hours",
        "location": {
            "city": "San Francisco",
            "state": "CA",
            "zipCode": "94103"
        },
        "travelPreferences": "Professional must travel to my address"
    },
    "customer": {
        "customerID": "437282427635040257",
        "name": "John Doe"
    },
    "business": {
        "businessID": "437282430088732672",
        "name": "Mr. Clean's Sparkly Cleaning Service"
    }
}
    print(thumbtack_json_to_pandas(test_dict))