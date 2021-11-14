from flask import Flask, request, jsonify, Response
from flask_httpauth import HTTPBasicAuth
from passlib.hash import sha256_crypt
import validators
#from thumbtack_conn import thumbtack_json_to_pandas
import json
import pandas as pd
import server.db as db
import server.helper as helper
from misc.thumbtack_conn import thumbtack_lead_json_to_pandas
import db
import helper
import uuid

app = Flask(__name__)
auth = HTTPBasicAuth()

app.config.from_pyfile('config.py')

database_url = app.config['DATABASE_URL']
db_obj = db.Database(database_url)


@auth.verify_password
def verify_password(username, password):
    user = json.loads(db_obj.get_data(db_schema='talking_potato', table_name='users', filter_data={'username': username}))
    if len(user) > 0  and sha256_crypt.verify(password, user[0]['password']):
        return username


@app.route("/")
def hello_world():
    result = db_obj.get_all_leads()
    df = pd.DataFrame(list(result.fetchall()))
    x = (df.to_json(orient="records"))
    return x


# TODO: initialize with the right business credentials/api keys

@app.route("/thumbtack_lead", methods=["POST"])
@auth.login_required
def receive_lead():
    print("data ", request.json)
    data = {"status": "success"}

    # process data and add to database

    return data, 200


@app.route("/thumbtack_messages", methods=["POST"])
@auth.login_required
def receive_message():
    print("data ", request.json)
    data = {"status": "success"}

    # process data and add to database

    return data, 200


@app.route("/register", methods=["POST"])
def register():
    email = request.args.get("email")
    username = request.args.get("username")
    password = request.args.get("password")
    email_query = json.loads(db_obj.get_data(db_schema='talking_potato', 
        table_name='users', filter_data={'email': email}))
    name_query = json.loads(db_obj.get_data(db_schema='talking_potato', 
        table_name='users', filter_data={'username': username}))
    if not validators.email(email):
        return {'status': 'bad email'}, 400 
    if len(username) < 3:
        return {'status': 'username too short'}, 400 
    if len(password) < 6:
        return {'status': 'password too short'}, 400 
    if not username.isalnum():
        return {'status': 'username must be alphanumeric'}, 400
    if len(email_query) > 0:
        return {'status': 'email already registered'}, 400
    if len(name_query) > 0:
        return {'status': 'username already registered'}, 400
        
    password_hash = sha256_crypt.encrypt(password)
    entry = {'user_id': str(uuid.uuid4()), 'username': username, 
        'password': password_hash, 'email': email}
    if request.args.get('phone_number'):
        entry['phone_number'] = request.args.get("phone_number")
    if request.args.get('thumbtack_user_id') and request.args.get('thumbtack_api_key'):
        entry['thumbtack_user_id'] = request.args.get('thumbtack_user_id')
        entry['thumbtack_api_key'] = request.args.get('thumbtack_api_key')
    if request.args.get('facebook_user_id') and request.args.get('fb_app_secret_key') \
            and request.args.get('fb_page_access_token'):
        entry['facebook_user_id'] = request.args.get('facebook_user_id')
        entry['fb_app_secret_key'] = request.args.get('fb_app_secret_key')
        entry['fb_page_access_token'] = request.args.get('fb_page_access_token')
    db_obj.insert_row('talking_potato', 'users', entry)
    return {'status': 'success'}, 200


APP_SECRET = '6726e5ccf4113b63275c1d6c86a0af3e'

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


@app.route("/fb_lead", methods=['GET', 'POST'])
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

                db_obj.insert_row('fb', 'messages', flat_msg)

        return Response(status=200)

    else:
        return Response(status=200)


@app.route("/get_messages", methods=['GET'])
def get_messages():
    filter_data = {}
    source = request.args.get('source')
    contacted_date = request.args.get('date')

    if source:
        source = source.replace("'", "")
        filter_data['user_source'] = source
    if contacted_date:
        contacted_date = contacted_date.replace("'", "")
        date_format_check = helper.check_date_format(contacted_date)
        if not date_format_check:
            return 'Please enter the date in YYYY-MM-DD format'
        filter_data['date(contacted_time)'] = contacted_date
    result = db_obj.get_data(db_schema='talking_potato', table_name='messages', filter_data=filter_data)
    return result


@app.route("/get_leads", methods=['GET'])
def get_leads():
    filter_data = {}
    contacted_date = request.args.get('date')

    if contacted_date:
        contacted_date = contacted_date.replace("'", "")
        date_format_check = helper.check_date_format(contacted_date)
        if not date_format_check:
            return 'Please enter the date in YYYY-MM-DD format'
        filter_data['date(contacted_time)'] = contacted_date
    result = db_obj.get_data(db_schema='thumbtack', table_name='leads', filter_data=filter_data)
    return result


if __name__ == '__main__':
    app.run(debug=True)
