from flask import Flask, request, jsonify

app = Flask(__name__)


class DataStore():
    data = {}

latest = DataStore()


@app.route('/api/update.json', methods=['POST'])
def update():
    content = request.json
    latest.data = content
    print("latest.data updated")
    print(latest.data)
    return "ok"


@app.route('/api/update.json', methods=['GET'])
def read():
    print(latest.data)
    return jsonify(latest.data)


print("ok")
