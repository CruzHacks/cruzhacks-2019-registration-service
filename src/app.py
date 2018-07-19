"""
[summary]
"""


from flask import Flask, jsonify

APP = Flask(__name__)


@APP.route("/", methods=["GET"])
def home():
    """
    [summary]

    Returns:
        [type]: [description]
    """

    return jsonify(
        code="200",
        message="Hello, World.",)


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=5000, debug=True)
