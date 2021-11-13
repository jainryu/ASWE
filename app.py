from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
#from thumbtack_conn import thumbtack_json_to_pandas

import pandas as pd
import db

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

if __name__ == '__main__':
    app.run(debug=True)


