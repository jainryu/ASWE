from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
#from thumbtack_conn import thumbtack_json_to_pandas

app = Flask(__name__)
auth = HTTPBasicAuth()

USER_DATA = {
    "jenna": "smith22"
}

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password

@app.route("/")
def hello_world():
    return "<p>Hello World!</p>"
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
def receive_lead():
    if not verify(request.authorization['username'], request.authorization['password']):
        return {'status': 'bad password'}, 401 
    print("data ", request.json)
    data = {"status": "success"}

    # process data and add to database

    return data, 200

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')


