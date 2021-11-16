'''
Integration Testing
'''
import json
from requests.auth import _basic_auth_str
import pytest
import db
from app import create_app


def create_api_string_from_dict(data):
    """
    Helper function to convert dictionary to api string
    """
    api_string = ''
    for key in data:
        api_string += key
        api_string += '='
        api_string += data[key]
        api_string += '&'
    api_string = api_string[:-1] if len(api_string) > 0 else ''
    return api_string


@pytest.fixture(scope="session", autouse=True)
def clear_tables():
    """
    Helper function that clears all tables before the test runs
    """
    db_obj = db.Database('postgresql+psycopg2://postgres:postgres@35.238.149.103/tp_test')
    db_obj.run_sql('TRUNCATE TABLE fb.messages;', False, True)
    db_obj.run_sql('TRUNCATE TABLE talking_potato.users;', False, True)
    db_obj.run_sql('TRUNCATE TABLE thumbtack.leads;', False, True)
    db_obj.run_sql('TRUNCATE TABLE thumbtack.messages;', False, True)


@pytest.fixture
def client():
    app = create_app('integ_test_config.py')
    with app.test_client() as client:
        yield client


def test_home_url(client):
    """
    Tests root url
    """
    response = client.get("/")
    assert b'Hello from Talking Potatoes!!!' in response.data


def test_register(client):
    """
    Tests registration with valid data
    """
    data = {
        'email': 'integ_test@gmail.com',
        'username': 'integtest',
        'password': 'integtest',
        'thumbtack_user_id': 'thumbtack_partner',
        'thumbtack_password': 'thumbt@ck!',
        'thumbtack_business_id': '286845156044809661'
    }
    api_string = create_api_string_from_dict(data)
    response = client.post("/register?{}".format(api_string))
    assert response.status_code == 200


def test_receive_messages(client):
    """
    Tests thumbtack_message endpoint with valid message
    """
    sample_message = {
        "leadID": "299614694480093245",
        "customerID": "331138063184986319",
        "businessID": "286845156044809661",
        "message": {
            "messageID": "8699842694484326245",
            "createTimestamp": "1498760294",
            "text": "Do you offer fridge cleaning or is that extra?"
        }
    }

    response = client.post('/thumbtack_message', headers={
    "Authorization": _basic_auth_str('integtest', 'integtest')}, data=sample_message)

    assert response.status_code == 200

def test_receive_leads(client):
    """
    Tests thumbtack_lead endpoint with valid lead
    """
    sample_lead = {
        "leadID": "299614694480093245",
        "createTimestamp": "1498760294",
        "request": {
            "requestID": "2999842694480093245",
            "category": "Interior Painting",
            "title": "Interior Painting",
            "description": "There is a stain on the door that needs to be touched up.",
            "schedule": "Date: Tue, May 05 2020\nTime: 6:00 PM\nLength: 3.5 hours",
            "location": {
            "city": "San Jose",
            "state": "CA",
            "zipCode": "95125"
            },
            "travelPreferences": "Professional must travel to my address.",
            "details": [
            {
                "question": "Type of property",
                "answer": "Home"
            },
            {
                "question": "Number of rooms",
                "answer": "4 rooms"
            }
            ]
        },
        "customer": {
            "customerID": "331138063184986319",
            "name": "John Davis",
            "phone": "1234567890"
        },
        "business": {
            "businessID": "286845156044809661",
            "name": "Tim's Painting Business"
        }
    }

    response = client.post('/thumbtack_lead', headers={
    "Authorization": _basic_auth_str('integtest', 'integtest')}, data=sample_lead)

    assert response.status_code == 200

def test_get_all_leads(client):
    """
    Tests get_leads endpoint query
    """
    response = client.get('/get_leads', headers={
         "Authorization": _basic_auth_str('integtest', 'integtest')})
    # data = json.loads(response.data)
    print(response)
    assert response.status_code == 200


def test_get_all_messages(client):
    """
    Tests get_messages endpoint query
    """
    response = client.get('/get_messages', headers={
         "Authorization": _basic_auth_str('integtest', 'integtest')})
    print(response)
    assert response.status_code == 200


def test_get_lead_analytics(client):
    """
    Tests lead_analytics endpoint with valid filter
    """
    filter = {
        'from_date': '2021-01-01',
        'to_date': '2021-11-15'
    }
    api_string = create_api_string_from_dict(filter)
    response = client.get('/lead_analytics?{}'.format(api_string),
                          headers={"Authorization": _basic_auth_str('integtest', 'integtest')})
    print(response)
    assert response.status_code == 200
    # assert len(data) == 10


def test_get_messages_analytics(client):
    """
    Tests message_analytics endpoint with valid filter
    """
    filter = {
        'from_date': '2021-01-01',
        'to_date': '2021-11-15'
    }
    api_string = create_api_string_from_dict(filter)
    response = client.get('/message_analytics?{}'.format(api_string),
                          headers={"Authorization": _basic_auth_str('integtest', 'integtest')})
    print(response)
    assert response.status_code == 200
