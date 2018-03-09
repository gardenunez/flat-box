from db import PostgresDb
from flask import Flask, jsonify, make_response, request
from flat_box_encoder import FlatBoxJsonEncoder

from apartments import get_apartments, load_apartments
from logger import get_logger


app = Flask(__name__)
app.json_encoder = FlatBoxJsonEncoder

logger = get_logger(__name__)

@app.errorhandler(Exception)
def handle_invalid_usage(exception):
    logger.error(str(exception), exc_info=True)
    return make_response(jsonify({'error': str(exception)}), 500)

@app.route("/apartments", methods=['GET'])
def list_apartments():
    longitude = request.args.get('lo')
    latitude = request.args.get('la')
    side = request.args.get('s')
    rooms = request.args.get('r')
    area = request.args.get('a')
    return jsonify(get_apartments(longitude=longitude,
                                  latitude=latitude,
                                  side=side,
                                  rooms=rooms,
                                  area=area))

@app.route("/", methods=['POST'])
def load():
    load_apartments()
    return make_response(jsonify(), 201)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, use_reloader=True)
