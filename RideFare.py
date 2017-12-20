#import pandas as pd
#import matplotlib.pyplot as plt
import numpy as np
import math
import requests
import os

# LYFT CLIENT SETUP
from lyft_rides.auth import ClientCredentialGrant
from lyft_rides.session import Session as lyftSession
lyft_token = os.environ.get('LYFT_TOKEN')
auth_flow = ClientCredentialGrant(client_id="BqM2cwqXmV3w", client_secret=lyft_token, scopes=set(["public"]))
lyft_session = auth_flow.get_session()
lyft_token = lyft_session.oauth2credential.access_token

from lyft_rides.client import LyftRidesClient
lyft_client = LyftRidesClient(lyft_session)

# UBER CLIENT SETUP
from uber_rides.session import Session as uberSession
from uber_rides.client import UberRidesClient
uber_token = os.environ.get('UBER_TOKEN')
uberSession = uberSession(server_token = uber_token)
uber_client = UberRidesClient(uberSession)



# list of apps to look for for price options
apps = ["Uber", "Lyft"]

#tuple representing destination latitude and longitude
main_start = (42.3601, -71.0942)
main_dest = (42.3471, -71.0825)
main_car_choice = "reg"
start_map = {}
end_map = {}

car_choices = {"reg": ["uberX","lyft"], "shared":["uberPOOL", "lyft_line"], 
                "fancy": ["UberBLACK", "lyft_lux"], "big": ["uberXL", "lyft_plus"]}

RIDE_TYPES = ["lyft", "lyft_line", "lyft_plus", "lyft_lux",
            "uberPOOL", "uberX", "uberXL", "UberBLACK" ]


#Maximum distance user is willing to walk in miles
#MAX_DIST = 5
inc_miles = 0.125


'''
Method to get miles in one degree of longitude from latitude
'''

def get_long_mi(latitude):
    return math.cos(latitude*math.pi/180)*69.172

'''
Method to get estimated price from app of choicer

args:
    -app: string representing which app pricing you're looking for
    -start_loc: tuple of (lat, long) of starting location

Returns:
    dictionary mapping travel options to price estimates {"string": tuple of floats (min, max)}

'''
def get_prices(app, start_loc, dest_loc):
    #dictionary which will map travel options to prices
    #i.e. "UberPool: $1000 "
    price_ops = {}
    if app == "Uber":
        price_ops = get_prices_uber(app, start_loc, dest_loc)
    elif app == "Lyft":
        price_ops = get_prices_lyft(app, start_loc, dest_loc)
    else:
        #throw an error if you make an invalid request?
        print("Error: Invalid app name...")
        return None

    return price_ops

'''
Helper function to get prices for Uber
args:
    -app: string representing which app pricing you're looking for
    -start_loc: tuple of (lat, long) of starting location

Returns:
    dictionary mapping travel options to price estimates {"string": tuple of floats (min, max)}
'''
def get_prices_uber(app, start_loc, dest_loc):
    price_ops = {}
    #use Uber API commands to get fare estimate
    uber_prices = uber_client.get_price_estimates(start_latitude = start_loc[0], 
        start_longitude = start_loc[1], 
        end_latitude = dest_loc[0], 
        end_longitude = dest_loc[1], 
        seat_count = 1).json["prices"] # TODO: later implementation account for multiple seats

    #print (type(uber_prices), uber_prices)

    for  travel_method in uber_prices:
        if travel_method["display_name"] in RIDE_TYPES:
            price = (travel_method["low_estimate"], travel_method["high_estimate"])
            price_ops[travel_method["display_name"]] = price
        else:
            #print(travel_method["display_name"])
            pass
    return price_ops

'''
Helper function for get prices for Lyft
args:
    -app: string representing which app pricing you're looking for
    -start_loc: tuple of (lat, long) of starting location

Returns:
    dictionary mapping travel options to price estimates {"string": tuple of floats (min, max)}
'''
def get_prices_lyft(app, start_loc, dest_loc):
    price_ops = {}
    #use lyft API to get fare estiamate
    # lyft_prices = lyft_client.get_cost_estimates(start_latitude = start_loc[0], 
    # start_longitude = start_loc[1], 
    # end_latitude = dest_loc[0], 
    # end_longitude = dest_loc[1])#.json["cost_estimates"] 
    start_latitude = start_loc[0] 
    start_longitude = start_loc[1] 
    end_latitude = dest_loc[0] 
    end_longitude = dest_loc[1]

    #lyft_url = "https://api.lyft.com/v1/cost?ride_type=lyft&start_lat="+str(start_latitude)+"&start_lng="+str(start_longitude)+"&end_lat="+str(end_latitude)+"&end_lng="+str(end_longitude)
    lyft_url = "https://api.lyft.com/v1/cost?start_lat=" + str(start_latitude)\
        + "&start_lng=" + str(start_longitude) \
        + "&end_lat=" + str(end_latitude) \
        + "&end_lng=" + str(end_longitude)

    lyft_request = requests.get(lyft_url, headers={'Authorization': "Bearer "+lyft_token})
    lyft_prices = lyft_request.json()["cost_estimates"]
    #print(lyft_prices)

    for travel_method in lyft_prices:
        # Only looking for certain types of rides 
        if travel_method["ride_type"] in RIDE_TYPES:
            price = (travel_method["estimated_cost_cents_min"]/100.0, 
                    travel_method["estimated_cost_cents_max"]/100.0)
            price_ops[travel_method["ride_type"]] = price
        else:
            #print (travel_method["ride_type"])
            #print(travel_method["display_name"])
            pass
    return price_ops

'''
Method to get neighboring tiles, within "willing to walk" distance
- Assumes only in one quadrant of the globe

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

    lng_conv = 1/get_long_mi(c_lat)

    #distance to increment by
    inc_dist = inc_miles * mi_to_deg

    #for diagonal neighbors
    v_leg = inc_dist # difference in lat
    h_leg = (3**0.5) * inc_miles * lng_conv #differnce in long

    top = (c_lat + 2*v_leg, c_lng)
    bot = (c_lat - 2*v_leg, c_lng)
    top_R = (c_lat + v_leg, c_lng + h_leg)
    bot_R = (c_lat - v_leg, c_lng + h_leg)
    top_L = (c_lat + v_leg, c_lng - h_leg)
    bot_L = (c_lat - v_leg, c_lng - h_leg)
    
    neighbors = [top, top_R, top_L, bot, bot_L, bot_R]

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
            self.price_ops[app_option] = get_prices(app_option, loc, dest)
        self.neighbors = get_neighbors(loc)

     



'''
Method to change destination location
'''
def set_start(st_loc):
    main_start = st_loc

'''
Method to change destination location
'''
def set_dest(des_loc):
    main_dest = des_loc

'''
Method to set car choice
'''
def set_car(your_ride):
    main_car_choice = your_ride


'''
Price Map

-"3D array"
    -x: start locs
    -y: end locs
    -z: ride options
    - point == price
-data structure mapping location information

- keys: Location tuples of (longitude, latitude)
- values:
    - price_ops - dictionary mapping app to price options
        -keys: app (i.e. "Uber", "Lyft", etc)
        -values: dictionary of methods and prices (i.e.(UberX : $100, etc))
    - neighbors
        -list of neighboring locations (based either on hex map or own neighbor pints)


{(star_lat, start_long): 
    {(end_lat, end_long): 
        {'type': (min, max) 
        ...
        }
    ...
    }
...
}
'''
PriceMap = {}


'''
Method to build 3D grid

args: 
    - start location
    - end location

Returns:
3D dictionary of prices based on starts, ends, and ride types
'''
def buildMap(p2p=True):
    pos_starts = [main_start]
    pos_ends = [main_dest]

    if not p2p:
        pos_starts.extend(get_neighbors(main_start))
        pos_ends.extend(get_neighbors(main_dest))

    for index in range(len(pos_starts)):
        start_map[index] = pos_starts[index]
        end_map[index] = pos_ends[index]

    for st in pos_starts:
        PriceMap[st]= {}
        for end in pos_ends:
            PriceMap[st][end]={}
            for app in apps:
                PriceMap[st][end].update(get_prices(app, st, end))
            #print (PriceMap[st][end])

    return PriceMap
    

'''
Method that returns the list of prices for a particular location given a car choice

args:
    -loc_role -string, either "start" or "dest", characterizes coordinates passed in
    -loc_num - an integer representing which number tile was selected
    -car - string, will map to car choices dictionary, i.e. "big" yields (UberXL, lyft_plus)

returns: 
    A list of LocationPrice Entries
    LocationPrice Entry 
    {
        "location":[lat, lng],
        "price":[uber, lyft]
    }
'''
def query_price(loc_role, loc_num, car_pick):
    price_results = {}
    cars = car_choices[car_pick] # Will be length of num apps
    
    if loc_role == "start":
        try:
            loc_coords = start_map[loc_num]
            #return the prices with this start node
            for end_loc in PriceMap[loc_coords]:
                found_prices = [None,None]
                for index in range(len(cars)):

                    if cars[index] in PriceMap[loc_coords][end_loc].keys():
                        min_price = PriceMap[loc_coords][end_loc][cars[index]][0]
                        found_prices[index]=float(min_price)

                price_results[end_loc] = tuple(found_prices)
        except KeyError as e:
            print("Key Error: " + str(e))
            print(start_map)


    elif loc_role == "dest":
        loc_coords = end_map[loc_num]
        #go through and find prices with this end node
        for start in PriceMap:
            found_prices = [None, None]
            for index in len(cars):
                if cars[index] in PriceMap[start][loc_coords].keys():
                    min_price = PriceMap[start][loc_coords][cars[index]][0]
                    found_prices[index] = float(min_price)
            price_results[start] = tuple(found_prices)
    else:
        #throw error saying, invalid entry
        print ("Invalid request.")

    return results2json(price_results)

def results2json(results):
    lo_results = []
    for location in results:
        price_tuple = results[location]
        entry = {"location": [float(location[0]), float(location[1])], 
                "prices":[float(price_tuple[0]), float(price_tuple[1])]}
        lo_results.append(entry)
    return lo_results


'''
A convenience function to convert a map object to valid json
Takes in a Map and returns the JSON equivalent. 

Equivalent is a list of price querys
[query1, query2, query3...]

PriceQuery is a dictionary with 3 named field: 
{   "start_loc": [lat, long], 
    "end_loc": [lat, long], 
    "prices": <entry>
}
An entry is dictionary of ride types to prices 
{'ride_type': [price low, price high], ...}

Coordinate is a 2 element list containing lat and long
[lat, long]

Prices is a 2 element list containing low and high prices
[low, high]
'''
def PriceMap2Json(myMap):
    json_map = []

    for start_loc in myMap:
        for end_loc in myMap[start_loc]:
            json_entry = {}
            for ride_type in myMap[start_loc][end_loc]:
                price_tuple = myMap[start_loc][end_loc][ride_type]
                json_entry[ride_type] = [price_tuple[0], price_tuple[1]]
                        
            json_start_loc = [start_loc[0], start_loc[1]]
            json_end_loc = [end_loc[0], end_loc[1]]

            this_query = {"start_loc":json_start_loc, 
                    "end_loc":json_end_loc,
                    "prices":json_entry}
            json_map.append(this_query)

    print(json_map)
    return json_map


if __name__ == "__main__":
    print("Base prices: \n")
    buildMap()
    
    #print(PriceMap[main_start][main_dest])
    #print()
    #PriceMap2Json(PriceMap)
    print(query_price("start", 0,"fancy"))
