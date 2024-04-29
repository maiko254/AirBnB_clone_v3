#!/usr/bin/python3
"""
   Creates a view for User objects that handles all default
   RESTful API actions
"""
from models import storage
from models.user import User
from flask import abort, request
from api.v1.views import app_views


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def users():
    """ Retrieves a list of all User objects """
    users = []
    for k, v in storage.all(User).items():
        users.append(v.to_dict())

    return users


@app_views.route("/users/<user_id>", methods=['GET'],
                 strict_slashes=False)
def user(user_id):
    """ Retrives a User object """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)

    return obj.to_dict()


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()

    return {}, 200


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def create_User():
    """ Creates a User object """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if 'email' not in content:
        abort(400, 'Missing email')
    if 'password' not in content:
        abort(400, 'Missing password')

    user = User(email=content['email'], password=content['password'])
    user.save()

    return user.to_dict(), 201


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def update_User(user_id):
    """ Updates a User object """
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)

    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')

    for k, v in content.items():
        if k not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(obj, k, v)

    obj.save()

    return obj.to_dict(), 200
