from flask import Flask
from flat_box_encoder import FlatBoxJsonEncoder

app = Flask(__name__)
app.json_encoder = FlatBoxJsonEncoder


from apartments import get_apartments, load_apartments
from db import PostgresDb
from flask import jsonify, make_response
CONNECTION_STR = 'postgresql://postgres:postgres@db/postgres'
@app.route("/")
def hello():
    db = PostgresDb(connection_str=CONNECTION_STR)
    return jsonify(get_apartments(db))

@app.route("/", methods=['POST'])
def load():
    db = PostgresDb(connection_str=CONNECTION_STR)
    load_apartments(db)
    return make_response(jsonify(), 201)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, use_reloader=True)
