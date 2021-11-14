from flask import Flask, request
import requests
import os

from application_services.lead_service import LeadService

app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = os.environ.get("APP_SECRET")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")

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

@app.route("/", methods=['GET', 'POST'])
def webhook():
    print('ok')
    if request.method == 'GET':
        return verify_webhook(request)

    elif request.method == 'POST':
        payload = request.json
        #print('payload: ', payload)
        event = payload['entry'][0]['messaging']
        for msg in event:
            if is_user_message(msg):
                text = msg['message']['text']
                temp = {'text': text}
                msg['message'] = temp
                LeadService.add_new_lead(msg)
                bot_response = get_bot_response(text)
                send_message(msg['sender']['id'], bot_response)

        return "Message received"

    else:
        return '200'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)