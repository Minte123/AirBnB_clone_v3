#!/usr/bin/python3
"""
    A module that contains index.py
"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """
        Displays the a json format message
    """
    if request.method == 'GET':
        response = {"status": "OK"}
        return jsonify(response)


@app_views.route('/stats', methods=['GET'])
def stats():
    """
        Returns the count of all objects
    """
    if request.method == 'GET':
        response = {}
        cls_dict = {
                        "Amenity": "amenities",
                        "City": "cities",
                        "Place": "places",
                        "Review": "reviews",
                        "State": "states",
                        "User": "users"
                    }
        for key, value in cls_dict.items():
            response[value] = storage.count(key)
        return jsonify(response)
