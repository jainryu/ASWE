import pytest
import requests
BASE_URL = 'https://tp-leads-app.herokuapp.com'


def test_invalid_user_receive_lead():
    'function returns 401 if provided password is incorrect'
    url = '{}/thumbtack_lead'.format(BASE_URL)
    req = requests.post(url, auth=('TEST', 'Incorrect'))
    assert req.status_code == 401


def test_valid_user_receive_lead():
    'function returns 200 if provided password is correct'
    url = '{}/thumbtack_lead'.format(BASE_URL)
    req = requests.post(url, auth=('TEST', 'TEST'))
    assert req.status_code == 200


def test_invalid_user_receive_message():
    url = '{}/thumbtack_messages'.format(BASE_URL)
    req = requests.post(url, auth=('TEST', 'Incorrect'))
    assert req.status_code == 401


def test_invalid_user_receive_message():
    url = '{}/thumbtack_messages'.format(BASE_URL)
    req = requests.post(url, auth=('TEST', 'TEST'))
    assert req.status_code == 200
