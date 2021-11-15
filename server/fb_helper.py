"""
facebook helper method
"""

def is_user_message(message):
    """verify that the message received is text (not image, etc)

    :return tuple: a tuple containing
        dict data: the thumbtack message data that was received
        int: response status code
    """
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))
