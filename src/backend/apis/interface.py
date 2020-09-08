from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from .search import search


app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route("/", methods=["POST", "GET"])
@cross_origin(supports_credentials=True)
def index():
    return jsonify([{'dialogue': 'ok'}])


app.route("/search", methods=["POST"])(
    cross_origin(supports_credentials=True)
    (search)
)
