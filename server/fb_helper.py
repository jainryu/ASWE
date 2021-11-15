def verify_webhook(req, username):
    """webhook verification required by facebook

    :param flask.Request req: the flask request object
    :return string: either the challenge received by facebook, or http status 400
    """
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
    """verify that the message received is text (not image, etc)

    :return tuple: a tuple containing
        dict data: the thumbtack message data that was received
        int: response status code
    """
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))