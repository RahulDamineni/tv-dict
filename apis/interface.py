from flask import Flask
from .search import search

app = Flask(__name__)
app.route("/search", methods=["POST"])(search)
