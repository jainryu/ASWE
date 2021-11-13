from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
#from thumbtack_conn import thumbtack_json_to_pandas

import pandas as pd
import db
import requests
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

USER_DATA = {
    "jenna": "smith22"
}
db_obj = db.Database()

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password

@app.route("/")
def hello_world():
    result = db_obj.get_all_leads()
    df = pd.DataFrame(list(result.fetchall()))
    x = (df.to_json(orient="records"))
    return x
# TODO: initialize with the right business credentials/api keys 

@app.route("/thumbtack_lead", methods=["POST"])
def receive_lead():
    if not verify(request.authorization['username'], request.authorization['password']):
        return {'status': 'bad password'}, 401 
    print("data ", request.json)
    data = {"status": "success"}

    # process data and add to database

    return data, 200

@app.route("/thumbtack_messages", methods=["POST"])
def receive_message():
    if not verify(request.authorization['username'], request.authorization['password']):
        return {'status': 'bad password'}, 401 
    print("data ", request.json)
    data = {"status": "success"}

    # process data and add to database

    return data, 200

APP_SECRET='6726e5ccf4113b63275c1d6c86a0af3e'

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = APP_SECRET
PAGE_ACCESS_TOKEN='EAANjKaTs280BAE8mOHrN4WUKsCByhXkpRxMKprDlSt0wpcPSKV2y954znFBJEiW8NWZAtfvtv2ht1NFjwwoGzw00VEPcQzBesKdqXmOqgM9HG6l1lwnGa1YF1jwcZAhs9J2I3gpbMw0POoNTj8vRF6MWG8IcgNbry6Htq7o3ZAEJkPyQgLxOg13y5fN5XQZD'

def verify_webhook(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')
    if token == VERIFY_TOKEN:
        print('verified')
        return str(challenge)
    return '400'

def send_message(recipient_id, bot_response):
    """Send a response to Facebook"""
    payload = {
        'message': {'text': bot_response},
        'recipient': {'id': recipient_id},
        'notification_type': 'regular'
    }

    auth = {'access_token': PAGE_ACCESS_TOKEN}

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()

def get_bot_response(message):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    return "This is a dummy response to '{}'".format(message)

def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))

@app.route("/fb_lead", methods=['GET','POST'])
def webhook():
    print('ok')
    if request.method == 'GET':
        return verify_webhook(request)

    elif request.method == 'POST':
        payload = request.json
        #print('payload: ', payload)
        # event = payload['entry'][0]['messaging']
        # for msg in event:
        #     if is_user_message(msg):
        #         text = msg['message']['text']
        #         temp = {'text': text}
        #         msg['message'] = temp
        #         LeadService.add_new_lead(msg)
        #         bot_response = get_bot_response(text)
        #         send_message(msg['sender']['id'], bot_response)

        return "Message received"

    else:
        return '200'

if __name__ == '__main__':
    app.run(debug=True)


