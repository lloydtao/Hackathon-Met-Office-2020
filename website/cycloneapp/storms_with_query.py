"""
Calculate the cyclones that pass through the radius of a point.
"""
import json
import sys
import time
import datetime

import geopy.distance

# Read a co-ordinate and radius.
# latitude = float(sys.argv[1])
# longitude = float(sys.argv[2])
# radius = float(sys.argv[3])
# input_file = sys.argv[4]

# # Populate cyclone nodes.
# nodes = 0
# max_nodes = 10000
# cyclone_nodes = []
# file = open(input_file, 'r')
# for line in file:
#     cyclone_nodes.append(line.strip().split(','))
#     if nodes > max_nodes:
#         print("WARNING: Input has over", max_nodes, "nodes. Only read first", max_nodes, "cyclone nodes.")
#         break
#     nodes = nodes + 1
# cyclone_nodes.pop(0)



# # End timer.
# end = time.time()
# seconds = round(end - start, 2)
# print("Time elapsed:", seconds, "seconds")

# location = "(" + str(latitude) + ", " + str(longitude) + ")."
# print(count, "cyclones have at least one node within", radius, "kilometres of", location)



# # Start timer.
# start = time.time()

from .models import Cyclone, CycloneNode

def query_storms(date_range, click_long, click_lat, radius):
    # Filter cyclones to within the date range
    date_split = date_range.split("-")
    min_date = datetime.date(int(date_split[0]), 1, 1)
    max_date = datetime.date(int(date_split[1]), 1, 1)
    dated_cyclones = Cyclone.objects.filter(datetime__range=(min_date, max_date))

    # If none match, return early
    if len(dated_cyclones) == 0: return {}

    # Get all cyclones nodes of all cyclones
    cyclone_nodes = []
    for cyclone in dated_cyclones:
        nodes = cyclone.nodes.all()
        
        cyclone_nodes.append(nodes)

    # Map cycle nodes to cyclones
    count = 0
    cyclones = {}
    cyclone = []
    last_key = cyclone_nodes[0].cyclone.sid

    for node in cyclone_nodes:
        current_key = node.cyclone.sid

        latitude = node.lat
        longitude = node.long
        intensity = node.intensity

        if current_key == last_key:
            cyclone.append([latitude, longitude, intensity])
        else:
            cyclones[last_key] = cyclone
            cyclone = [[latitude, longitude, intensity]]
            last_key = current_key

    # Create a list of SIDs that have at least one node within boundaries.
    SIDs_in_radius = ['']
    for node in cyclone_nodes:
        # Calculate distance
        coords_user = (click_lat, click_long)
        coords_node = (node.lat, node.long)
        distance = geopy.distance.distance(coords_user, coords_node).km

        # Check within boundary
        if distance < radius:
            if not node.cyclone.sid == SIDs_in_radius[-1]:
                SIDs_in_radius.append(node.cyclone.sid)
                count = count + 1

    SIDs_in_radius.pop(0)

    # Filter cyclones and their nodes for if they're within radius
    filtered_cyclones = {}
    for SID in SIDs_in_radius:
        filtered_cyclones[SID] = cyclones[SID]
    
    return filtered_cyclones