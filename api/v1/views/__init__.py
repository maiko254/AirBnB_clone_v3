#!/usr/bin/python3
""" Creates a blueprint app_views used in a flask web application """
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
