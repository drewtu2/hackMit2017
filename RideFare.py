import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#LYFT CLIENT SETUP
from lyft_rides.auth import ClientCredentialGrant
from lyft_rides.session import Session

auth_flow = ClientCredentialGrant(client_id=BqM2cwqXmV3w, client_secret=5uDeLNgJNRKb3n9Gg0BMEouzYphZjI9X, scopes=YOUR_PERMISSION_SCOPES)

from lyft_rides.client import LyftRidesClient

lyft_session = auth_flow.get_session()
lyft_client = LyftRidesClient(lyft_session)
#{"token_type": "Bearer", "access_token": "XgOzXKLM6Oj/tTRdyndXpJMC6+UOvXQxAnmNJaaWwY2aJFXWqD2pJLxJ2uPWcmfbL2Y+yL87IFYzT7OE/EEjwf75DEq5U9qfCzplImiACUV91ikGBtuiIqs=", "expires_in": 86400, "scope": "public"}
#lyft_token = XgOzXKLM6Oj/tTRdyndXpJMC6+UOvXQxAnmNJaaWwY2aJFXWqD2pJLxJ2uPWcmfbL2Y+yL87IFYzT7OE/EEjwf75DEq5U9qfCzplImiACUV91ikGBtuiIqs=

#UBER CLIENT SETUP
from uber_rides.session import session
from uber_rides.client import UberRidesClient

uber_token = eWfH_tAQpYHHfVi2nCSFbLrLpoS_69f34ldS63J0
session = Session(server_token = <uber_token>)
uber_client = UberRidesClient(session)

#list of apps to look for for price options
apps = ["Uber", "Lyft"]

#tuple representing destination latitude and longitude
dest = (1,1);

#Maximum distance user is willing to walk in miles
MAX_DIST = 5;
inc_miles = 1;


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
	dictionary mapping travel options to price estimates {"stirng": tuple of floats (min, max)}

'''
def getPrices(app, start_loc):
	#dictionary which will map travle options to prices
	#i.e. "UberPool: $1000 "

	price_ops = {}
	if app == "Uber":
		#use Uber API commands to get fare estimate
		uber_prices = uber_client.get_price_estimates(start_latitude = loc[0], 
		start_longitude = loc[1], 
		end_latitude = dest[0], 
		end_longitude = dest[1], 
		seat_count = 1)["prices"] #later implementation account for multiple seats

		for  travel_method in uber_prices:
			#add in change from strings to floats for uber
			price = ( travel_method["low_estimate"],travel_method["high_estimate"])
			price_ops[travel_method["display_name"]] = price
	elif app == "Lyft":
		#use lyft API to get fare estiamate
		lyft_prices = lyft_client.get_cost(start_lat = loc[0], 
		start_lng = loc[1], 
		end_lat = dest[0], 
		end_lng = dest[1])["cost_estimates"] 
		for travel_method in lyft_prices:
			#add lines to seperate max and min to be the parts of the tuple
			price = (travel_method["estimated_cost_cents_min"]/100.0, travel_method["estimated_cost_cents_max"]/100.0)
			price_ops[travel_method["ride_type"]] = price


	else:
		#throw an error if you make an invalid request?
		return

	return price_ops



'''
Method to get neighboring tiles, within "willing to walk" distance
-Assumes only in one quadrant of the globe

args: 
	-center_loc - tuple, (lat, long) point at the center of the hex
	

Returns:
	list of tuples representing 6 neighbors
'''
def get_neighbors(center_loc):

	c_lat = center_loc[0]
	c_lng = center_loc[1]

	#conversion factor
	mi_to_deg = 1/69

	#distance to increment by
	inc_dist = inc_miles * mi_to_deg

	#for diagonal neighbors
	v_leg = inc_dist # difference in lat
	h_leg = (3**0.5) * inc_dist #differnce in long

	top = (c_lat + 2*v_leg, c_lng)
	bot = (c_lat - 2*v_leg, c_lng)
	top_R = (c_lat + v_leg, c_lng + h_leg)
	bot_R = (c_lat - v_leg, c_lng + h_leg)
	top_L = (c_lat + v_leg, c_lng - h_leg)
	bot_L = (c_lat - v_leg, c_lng - h_leg)
	
	neighbors = [top, bot, top_R, bot_R, top_L, bot_L]

	return neighbors




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
		self.neighbors = get_neighbors(loc)

	 




'''
Method to create tile
'''
def create_tile(loc):
	return loc_tile(loc);

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


