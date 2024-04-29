#!/usr/bin/python3
"""
   Creates a new view for City objects that handles all default RESTFul API
   actions
"""
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, request


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """ Retrieves a list of all City objects of a State """
    obj = storage.get(State, state_id)
    cities_list = []
    if obj is None:
        abort(404)

    for city in obj.cities:
        cities_list.append(city.to_dict())

    return cities_list


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Retrieves a City object """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    return obj.to_dict()


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object matching with the given id """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()

    return {}, 200


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def create_City(state_id):
    """ Creates a City object linked to a State """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if 'name' not in content:
        abort(400, 'Missing name')

    new_city = City(state_id=state.id, name=content['name'])
    new_city.save()

    return new_city.to_dict(), 201


@app_views.route("/cities/<city_id>", methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """ updates a City record """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    for k, v in content.items():
        if k != 'id' or k != 'updated_at' or k != 'created_at':
            setattr(city, k, v)
    city.save()

    return city.to_dict(), 200
