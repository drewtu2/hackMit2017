from flask import Flask, request, jsonify
from time import sleep

#import csv
import requests
import threading
import json

import RideFair

from datetime import datetime
from io import StringIO

app = Flask(__name__, static_url_path="")
# NOT needed for demo

@app.route("/")
def run_app():
	return "Hello, world"

@app.route("/<path:path>")
def status_file(path):
	return app.send_static_file(path)


#change start or dest
@app.route("/api/seed", methods=['POST'])
def set_loc():
	coordinates = request.get_json(force=True)
    #start
    set_start(coordinates["start_coord"])
    set_dest(coordinates["end_coord"])
    buildMap()
    return

#change loc
@app.route("/api/change_loc/", methods=['POST'])
def change_loc():
	params = request.get_json(force=True)

    #start
    if params[node] = "start":
    	set_start(new_coord)
    else:
    	set_dest(new_coord)
    
    return

#change car
@app.route("/api/ride/", methods=['POST'])
def change_car():
	ride_type = request.get_json(force=True)
    return set_car(new_car)

#query prices
@app.route("/api/prices", methods=['POST'])
def get_price_list():

    params = request.get_json(force=True)
    return query_prices(params[role], params[coords], params[car])
