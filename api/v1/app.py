#!/usr/bin/python3
""" Starts a web flask application """
from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """ closes the storage on teardown """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Handles a 404 error """
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    host1 = os.getenv('HBNB_API_HOST')
    port1 = os.getenv('HBNB_API_PORT')
    if not host1:
        host1 = '0.0.0.0'
    if not port1:
        port1 = 5000
    app.run(host=host1, port=port1, threaded=True)
