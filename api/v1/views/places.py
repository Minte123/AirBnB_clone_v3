#!/usr/bin/python3
"""
    A module for creating new vew for Place obj
"""

from flask import Flask, make_response, request, abort, jsonify
from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_get(city_id):
    """
        Gets all the places from a specifc city provided with ID
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def place_get_with_id(place_id):
    """
        Gets a place with a specific ID
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_with_id_delete(place_id):
    """
        deletes a specific place with specific ID
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """
        create a new place
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    json_req = request.get_json()
    if 'user_id' not in json_req:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'name' not in json_req:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    user = storage.get("User", json_req['user_id'])
    if user is None:
        abort(404)
    json_req['city_id'] = city_id
    place = Place(**json_req)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def place_put(place_id):
    """
        updates the place obj
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())
