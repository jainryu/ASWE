import requests
from requests.auth import HTTPBasicAuth
import base64


auth = HTTPBasicAuth('animeshbhasin', 'animeshbhasin')

def test_home_url():
    response = requests.get('https://tp-leads-app.herokuapp.com:5000')
    assert response.text == 'Hello from Talking Potatoes!!!'
#
def test_get_messages():
    response = requests.get('https://tp-leads-app.herokuapp.com/get_leads',auth=auth)
    print (response.text)
#
test_get_messages()



