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

# find the modifier for x and y, this should give us a 0-1 range of where a point can be
    top_0_factor = 1/locations["top"][0]
    top_1_factor = 1/locations["top"][1]

# set the maxes to 1
    locations["top"][0] = 1
    locations["top"][1] = 1

    for location in [x for x in locations if x != "bottom" and x!= "top"]:
        locations[location][0] = locations[location][0] * top_0_factor
        locations[location][1] = locations[location][1] * top_1_factor


    # for location in locations:
    #     locations[location][0] =

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
