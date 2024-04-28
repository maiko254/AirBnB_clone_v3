#!/usr/bin/python3
""" creates web flask application with the route /status """
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """ route that returns the status of the REST api """
    return {
        "status": "OK"
    }
