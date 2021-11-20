import json

from flask import Flask
from flask import request, jsonify


app = Flask(__name__)


@app.route("/", methods=["GET"])
def speak_with_gasya():

    return "ну, блин("


if __name__ == "__main__":
    app.run(host="localhost", port=9111, debug=True)
