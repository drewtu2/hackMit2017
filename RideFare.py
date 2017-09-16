import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from uber_rides.session import session
from uber_rides.client import UberRidesClient

session = Session(server_token = <TOKEN>)
client = UberRidesClient(session)

#list of apps to look for for price options
apps = ["Uber", "Lyft"]

#tuple representing destination latitude and longitude
dest = (1,1);

'''
Price Map

-data structure mapping location information

-keys: Location tuples of (longitude, latitude)
-values:
	-price_ops - dictionary mapping app to price options
		-keys: app (i.e. "Uber", "Lyft", etc)
		-values: dictionary of methods and prices (i.e.(UberX : $100, etc))
	-neighbors
		-list of neighboring locations (based either on hex map or own neighbor pints)
'''
PriceMap = pd.DataFrame()


'''
Method to get estimated price from app of choice

args:
	-app - string representing which app pricing you're looking for
	-start_loc - tuple of (lat, long) of starting location

Returns:
	dictionary mapping travel options to price estimates {"stirng": "string"}

'''
def getPrices(app, start_loc):
	#dictionary which will map travle options to prices
	#i.e. "UberPool: $1000 "

	price_ops = {}
	if app == "Uber":
		#use Uber API commands to get fare estimate
		uber_prices = client.get_price_estimates(start_latitude = loc[0], 
		start_longitude = loc[1], 
		end_latitude = dest[0], 
		end_longitude = dest[1], 
		seat_count = 1) #later implementation account for multiple seats

		for  travel_method in uber_prices:
			price_ops[travel_method["display_name"]] = travel_method["estimate"]

	elif app == "Lyft":
		#use lyft API to get fare estiamate

	else:
		#throw an error if you make an invalid request?
		return

	return price_ops





'''
Class to store location information as object, tile?
args: 
	-loc, tuple of latitude and longitude of tile, representing start tile
'''
class loc_tile (object):
	def __init__(self, loc):
		self.loc = loc
		self.dest = dest #global?
		self.price_ops = {}
		for app_option in apps:
			self.price_ops[app_option] = getPrices(app_option, loc)
		self.neighbors = getNeighbors(loc)

	 




'''
Method to create tile
'''
def create_tile(loc):
	return 

'''
Method to add tile to price map

Steps:
-create tile
-update data structure
'''
def add_new_tile(loc):


'''
Method to change destination location
'''
def set_dest(des_loc):


