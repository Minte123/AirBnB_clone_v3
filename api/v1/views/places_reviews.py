#!/usr/bin/python3
"""
    A module for the new view of Review obj
"""

from flask import make_response, request, abort, jsonify
from models import storage
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_get(place_id):
    """
        Gets all the reviews from a specifc place provided with ID
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_reviews_with_id(review_id):
    """
        Gets a review obj with a specific ID
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_with_id(review_id):
    """
        deletes a review obj with a specifc ID
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review_with_id(place_id):
    """
        creats a review for a specific place
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    json_req = request.get_json()
    if 'user_id' not in json_req:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get("User", json_req['user_id'])
    if user is None:
        abort(404)
    if 'text' not in json_req:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    json_req['place_id'] = place_id
    review = Review(**json_req)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review_with_id(review_id):
    """
        updates the review obj
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
