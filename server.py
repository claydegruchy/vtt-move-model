from flask import Flask, request, jsonify,send_file
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


class DataStore():
    data = {}

latest = DataStore()

def make_relative(locations):
    for location in locations:
        locations[location][0] = locations[location][0] - locations["bottom"][0]
        locations[location][1] = locations[location][1] - locations["bottom"][1]

    return locations



@app.route('/api/update.json', methods=['POST'])
def update():
    content = request.json
    latest.data = content
    # print("latest.data updated")
    # print(latest.data)
    return "ok"


@app.route('/api/update.json', methods=['GET'])
@cross_origin()
def read():
    print(latest.data)

    return jsonify(make_relative(latest.data))


@app.route('/api/snapshot.jpg', methods=['GET'])
@cross_origin()
def send():
    return send_file("snapshot.jpg", mimetype='image/jpeg')



print("ok")
