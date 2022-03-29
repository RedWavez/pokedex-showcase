from flask import Flask, request
from settings.database import DB
from flask_cors import CORS
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def hello():
    return '<h1>Hello, André!</h1>'


@app.route('/pokemon/', methods=['GET'])
def pokemon():
    """
    Gets pokemon data
    :return:
    """
    args = request.args.to_dict()
    data = []

    query = "SELECT * FROM pokemon WHERE"
    if args.get('Name', None):
        query += " name=%s"
        data.append(args.get("name"))
    if args.get('id', None):
        query += " ID=%s"
        data.append(int(args.get("id")))
    query += " LIMIT 1"
    cursor = DB.cursor()
    cursor.execute(query, tuple(data))
    x = cursor.fetchall()
    return json.dumps(x)


if __name__ == 'main':
    app.run()
