from flask import Flask, request
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine('postgresql+psycopg2://postgres:postgres@35.238.149.103/tp')

app = Flask(__name__)

@app.route("/")
def hello():
    # return "Hello World!"
    result = engine.execute(
        "select * from thumbtack.test;"
    )
    df = pd.DataFrame(list(result.fetchall()))
    x = (df.to_json(orient="records"))
    return x


if __name__ == '__main__':
    app.run()