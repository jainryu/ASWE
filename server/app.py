from flask import Flask, request, Response
from flask_httpauth import HTTPBasicAuth
from thumbtack_conn import thumbtack_lead_json_to_list, thumbtack_message_json_to_list, create_test_data
from passlib.hash import sha256_crypt
import validators
import json
import pandas as pd
import db
import helper
import uuid
import analytics

app = Flask(__name__)
auth = HTTPBasicAuth()

app.config.from_pyfile('config.py')

database_url = app.config['DATABASE_URL']
db_obj = db.Database(database_url)

analytics_obj = analytics.Analytics(database_url)


@auth.verify_password
def verify_password(username, password):
    user = json.loads(
        db_obj.get_data(db_schema='talking_potato', table_name='users', filter_data={'username': username}))
    if len(user) > 0 and sha256_crypt.verify(password, user[0]['password']):
        return username


@app.route("/")
def hello_world():
    result = db_obj.get_all_leads()
    df = pd.DataFrame(list(result.fetchall()))
    x = (df.to_json(orient="records"))
    return x


# TODO: initialize with the right business credentials/api keys

@app.route("/dummy_thumbtack_lead", methods=["GET"])
def create_dummy_data():
    dummy_dict = create_test_data()
    data, column_names = thumbtack_lead_json_to_list(dummy_dict)
    db_obj.insert_row_from_list("thumbtack", "leads", data, column_names)

    return dummy_dict, 200


@app.route("/thumbtack_lead", methods=["POST"])
@auth.login_required
def receive_lead():
    data = {"status": "success"}

    data, column_names = thumbtack_lead_json_to_list(request.json)
    db_obj.insert_row_from_list("thumbtack", "leads", data, column_names)

    return data, 200


@app.route("/thumbtack_messages", methods=["POST"])
@auth.login_required
def receive_message():
    data = {"status": "success"}

    data, column_names = thumbtack_message_json_to_list(request.json)
    db_obj.insert_row_from_list("thumbtack", "messages", data, column_names)

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


# APP_SECRET = '6726e5ccf4113b63275c1d6c86a0af3e'

# FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
# VERIFY_TOKEN = APP_SECRET


def verify_webhook(req, username):
    query = json.loads(db_obj.get_data(db_schema='talking_potato', 
        table_name='users', filter_data={'username': username}))
    verify_token = query[0]['fb_app_secret_key']
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')
    if token == verify_token:
        print('verified')
        return str(challenge)
    return '400'


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))


@app.route("/fb_lead", methods=['GET', 'POST'])
@auth.login_required
def webhook():
    print('ok')
    if request.method == 'GET':
        return verify_webhook(request, auth.current_user())

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
@auth.login_required
def get_messages():
    username = auth.current_user()
    filter_data = {}
    source = request.args.get('source')
    contacted_date = request.args.get('date')
    #TODO: filter on the user
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
@auth.login_required
def get_leads():
    username = auth.current_user()
    query = json.loads(db_obj.get_data(db_schema='talking_potato', 
        table_name='users', filter_data={'username': username}))
    filter_data = {}
    filter_data['thumbtack_business_id'] = query[0]['thumbtack_business_id']
    contacted_date = request.args.get('date')

    if contacted_date:
        contacted_date = contacted_date.replace("'", "")
        date_format_check = helper.check_date_format(contacted_date)
        if not date_format_check:
            return 'Please enter the date in YYYY-MM-DD format'
        filter_data['date(contacted_time)'] = contacted_date
    result = db_obj.get_data(db_schema='thumbtack', table_name='leads', filter_data=filter_data)
    return result


@app.route("/message_analytics", methods=['GET'])
def get_message_analytics():
    filter_data = {}
    filter_date_range = []
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    dimension = request.args.get('dimension')

    filter_data['date(contacted_time)'] = 1

    if dimension:
        if dimension == 'user_source':
            filter_data['user_source'] = 1
        else:
            return 'Accepted value of dimension = user_source'

    if not from_date:
        from_date = '1900-01-01'
    else:
        from_date = from_date.replace("'", "")
        date_format_check = helper.check_date_format(from_date)
        if not date_format_check:
            return 'Please enter the date in YYYY-MM-DD format'
    filter_date_range.append(from_date)

    if not to_date:
        to_date = helper.get_todays_date_str()
    else:
        to_date = to_date.replace("'", "")
        date_format_check = helper.check_date_format(to_date)
        if not date_format_check:
            return 'Please enter the date in YYYY-MM-DD format'
    filter_date_range.append(to_date)
    result = analytics_obj.get_grouped_by_date(db_schema='talking_potato', table_name='messages',
                                               filter_data=filter_data, filter_date_range=filter_date_range)
    return result


@app.route("/lead_analytics", methods=['GET'])
def get_lead_analytics():
    filter_data = {}
    filter_date_range = []
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    dimension = request.args.get('dimension')

    filter_data['date(contacted_time)'] = 1

    if dimension:
        if dimension in ('category', 'state'):
            filter_data[dimension] = 1
        else:
            return 'Accepted values of dimension = category or state'

    if not from_date:
        from_date = '1900-01-01'
    else:
        from_date = from_date.replace("'", "")
        date_format_check = helper.check_date_format(from_date)
        if not date_format_check:
            return 'Please enter the date in YYYY-MM-DD format'
    filter_date_range.append(from_date)

    if not to_date:
        to_date = helper.get_todays_date_str()
    else:
        to_date = to_date.replace("'", "")
        date_format_check = helper.check_date_format(to_date)
        if not date_format_check:
            return 'Please enter the date in YYYY-MM-DD format'
    filter_date_range.append(to_date)
    result = analytics_obj.get_grouped_by_date(db_schema='thumbtack', table_name='leads',
                                               filter_data=filter_data, filter_date_range=filter_date_range)
    return result


if __name__ == '__main__':
    app.run(debug=True)
