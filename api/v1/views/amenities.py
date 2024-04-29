#!/usr/bin/python3
"""
   Creates a view for Amenity objects that handles all default
   RESTful API actions
"""
from models import storage
from models.amenity import Amenity
from flask import abort, request
from api.v1.views import app_views


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def amenities():
    """ Retrieves a list of all Amenity objects """
    amenities = []
    for k, v in storage.all(Amenity).items():
        amenities.append(v.to_dict())

    return amenities


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def amenity(amenity_id):
    """ Retrives an Amenity object """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)

    return obj.to_dict()


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an Amenity object """
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)

    storage.delete(obj)
    storage.save()

    return {}, 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_Amenity():
    """ Creates an Amenity object """
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if 'name' not in content:
        abort(400, 'Missing name')

    amenity = Amenity(name=content['name'])
    amenity.save()

    return amenity.to_dict(), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_Amenity(amenity_id):
    """ Updates an Amenity object """
    obj = storage.get(Amenity, amenity_id)
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
