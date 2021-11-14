from flask import Flask, request, jsonify, Response
from flask_httpauth import HTTPBasicAuth
#from thumbtack_conn import thumbtack_json_to_pandas
import pandas as pd
import db
import helper

app = Flask(__name__)
auth = HTTPBasicAuth()

USER_DATA = {
    "jenna": "smith22"
}

app.config.from_pyfile('config.py')

database_url = app.config['DATABASE_URL']
db_obj = db.Database(database_url)

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


def verify_webhook(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')
    if token == VERIFY_TOKEN:
        print('verified')
        return str(challenge)
    return '400'

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
        # print('payload: ', payload)
        event = payload['entry'][0]['messaging']
        for msg in event:
            if is_user_message(msg):
                text = msg['message']['text']
                temp = {'text': text}
                msg['message_id'] = msg['message']['mid']
                msg['message'] = temp
                msg['page_id'] = payload['entry'][0]['id']
                msg['update_time'] = payload['entry'][0]['time']
                flat_msg = helper.flatten_json(msg)
                flat_msg['update_time'] = helper.convert_epoch_milliseconds_to_datetime_string(flat_msg['update_time'])
                flat_msg['timestamp'] = helper.convert_epoch_milliseconds_to_datetime_string(flat_msg['timestamp'])

                db_obj.insert_row('fb','messages',flat_msg)

        return Response(status=200)

    else:
        return Response(status=200)

if __name__ == '__main__':
    app.run(debug=True)


