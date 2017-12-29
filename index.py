from flask import Flask, request, jsonify, Response, redirect
from time import sleep

#import csv
import requests
import threading
import json
import os

import RideFare as rf

from datetime import datetime
from io import StringIO

app = Flask(__name__, static_url_path="")
# NOT needed for demo

@app.before_request
def before_request():
    if not request.is_secure:
        print("Request insecure.... redirecting to https")
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)
    else:
        print("Secure request received....")

@app.route("/")
def run_app():
    return app.send_static_file("index.html")

@app.route("/<path:path>")
def status_file(path):
    return app.send_static_file(path)

#change start or dest
@app.route("/api/seed/", methods=['POST'])
def set_loc():
    params = request.get_json(force=True)
    start_coord = params["startCoord"]
    end_coord = params["endCoord"]
    MyPriceMap = {}
    

    print("set_loc: " + str(start_coord[0]) + ", " + str(start_coord[1]))
    
    #rf.set_start(params["startCoord"])
    #rf.set_dest(params["endCoord"])
    
    MyPriceMap = rf.buildMap(start_loc = start_coord, end_loc = end_coord)
    pmap_json = rf.PriceMap2Json(MyPriceMap)
    return jsonify(pmap_json);

#change loc
@app.route("/api/change_loc/", methods=['POST'])
def change_loc():
    params = request.get_json(force=True)

    #start
    if params[node] == "start":
        rf.set_start(new_coord)
    else:
        rf.set_dest(new_coord)
    rf.buildMap() 
    return jsonify({"status":200});

#change car
@app.route("/api/ride/", methods=['POST'])
def change_car():
    ride_type = request.get_json(force=True)
    rf.set_car(ride_type)
    return jsonify({"status":200});


#query prices
@app.route("/api/prices/", methods=['POST'])
def get_price_list():

    params = request.get_json(force=True)
    print(params)
    prices = rf.query_price(params["location-role"], params["location"], params["car_pick"])
    print("Got Prices: " + str(prices))
    
    return jsonify(prices[0])

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
