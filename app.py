import json

from flask import Flask
from flask import request, jsonify


app = Flask(__name__)


@app.route("/")
@app.route("/home")
def index():

    return jsonify({"answer": 123})


if __name__ == "__main__":
    app.run(host="localhost", port=9111, debug=True)
