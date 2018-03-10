from flask import Flask, jsonify, make_response, request, Response

from apartments import get_apartments, load_apartments, format_apartments_to_csv
from flat_box_encoder import FlatBoxJsonEncoder
from logger import get_logger

app = Flask(__name__)
app.json_encoder = FlatBoxJsonEncoder

logger = get_logger(__name__)


@app.errorhandler(Exception)
def handle_invalid_usage(exception):
    logger.error(str(exception), exc_info=True)
    return make_response(jsonify({'error': str(exception)}), 500)


@app.route("/", methods=['GET'])
def hello():
    return jsonify({'hello': 'world'})


@app.route("/apartments", methods=['GET'])
def list_apartments():
    # TODO: no validations are all
    longitude = request.args.get('lo')
    latitude = request.args.get('la')
    side = request.args.get('s')
    rooms = request.args.get('r')
    area = request.args.get('a')
    accept_header = request.headers.get('Accept')
    apartments = get_apartments(longitude=longitude, latitude=latitude,
                                      side=side, rooms=rooms, area=area)
    if not accept_header or accept_header == 'application/json':
        return jsonify(apartments)
    if accept_header == 'text/csv':
        csv_text = format_apartments_to_csv(apartments)
        return Response(
            csv_text,
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=apartments.csv"})

    if accept_header == 'application/pdf':
        return Response(
            'pdf_file',
            mimetype="application/pdf",
            headers={"Content-disposition": "attachment; filename=apartments.pdf"})

    return jsonify(apartments)

@app.route("/apartments", methods=['POST'])
def load():
    load_apartments()
    return make_response(jsonify(), 201)

if __name__ == "__main__":
    app.run(host='0.0.0.0', use_reloader=True)
