#!/usr/bin/python3
"""
   Create a new view for State objects that handles all default RESTFul
   API actions
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def all_states():
    """ Retrieves list of all State records in storage """
    states_list = []
    for k, v in storage.all(State).items():
        states_list.append(v.to_dict())
    return states_list


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def state_obj(state_id):
    """ Retrieves a State record with a matching state id """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return obj.to_dict()


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State record with the given id """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return {}, 200


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_State():
    """ creates a State record """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if 'name' not in content:
        abort(400, 'Missing name')
    new_state = State(name=content['name'])
    new_state.save()

    return new_state.to_dict(), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ update the State record matching the  given State id """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)

    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    for k, v in content.items():
        if k != 'id' or k != 'created_at' or k != 'updated_at':
            setattr(obj, k, v)
    obj.save()

    return obj.to_dict(), 200
