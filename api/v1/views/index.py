#!/usr/bin/python3
""" creates web flask application with the route /status """
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def api_status():
    """ route that returns the status of the REST api """
    return {
        "status": "OK"
    }


@app_views.route('/stats')
def count_objs():
    """ retrieves the number of each objects in storage by type """
    from models.user import User
    from models.place import Place
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.review import Review

    return {
        "users": storage.count(User),
        "amenities": storage.count(Amenity),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "cities": storage.count(City),
        "places": storage.count(Place)
    }
