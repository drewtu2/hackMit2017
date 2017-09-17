from flask import Flask, request, jsonify
from time import sleep
import pickle

#import csv
import requests
import threading
import json

import RideFair as rf

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
@app.route("/api/seed/", methods=['POST'])
def set_loc():
    coordinates = request.get_json(force=True)
    #start
    print(coordinates)
    rf.set_start(coordinates["startCoord"])
    rf.set_dest(coordinates["endCoord"])
    rf.buildMap()

    return jsonify({"status":200});

#change loc
@app.route("/api/change_loc/", methods=['POST'])
def change_loc():
    params = request.get_json(force=True)

    #start
    if params[node] == "start":
        rf.set_start(new_coord)
    else:
        rf.set_dest(new_coord)
    
    return jsonify({"status":200});

#change car
@app.route("/api/ride/", methods=['POST'])
def change_car():
    ride_type = request.get_json(force=True)
    return rf.set_car(ride_type)

#query prices
@app.route("/api/prices/", methods=['POST'])
def get_price_list():

    params = request.get_json(force=True)
    prices = rf.query_prices(params["location-role"], params["location"], params["car_pick"])
    print(prices)
    return {
           "keys": lol(prices.keys()),
           "values": lol(prices.values())}
# Tuple to List 
def tuple2List(tup):
    return [tup[0], [1]]

def lol(lot):
    alist = []
    for tup in lot:
        alist.append(tuple2List(tup))
        return [tuple2List(tup)]


