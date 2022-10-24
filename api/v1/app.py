#!/usr/bin/python3
"""
    A module to start a flask app
"""
from flask import Flask, request, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def tear_down(exception):
    """
        clsoses the connection
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """
        Handles the 404 not found error
    """
    error_code = exception.__str__().split()[0]
    text_msg = {"error": "Not found"}
    return make_response(jsonify(text_msg), error_code)


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
