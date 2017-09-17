from flask import Flask, request, jsonify
from time import sleep

#import csv
import requests
import threading
import json

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

