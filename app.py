from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    return jsonify({}), 204

@app.route("/api", methods=["POST"])
def start_analysis():
    # body = request.json()
    return jsonify({}), 200
