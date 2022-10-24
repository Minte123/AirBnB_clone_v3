#!/usr/bin/python3
"""
    A modules that returns an obj into a valid JSON
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import Flask, request, make_response, jsonify, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_with_no_id():
    """
        handles the http get request for states provided with no id
    """
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def states_with_id(state_id):
    """
        gets the state with a particular Id
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_delete(state_id):
    """
        deletes a specific state
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def state_post():
    """
        posts/creates new state
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def state_put(state_id):
    """
        handles to update a state with specifc id
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
