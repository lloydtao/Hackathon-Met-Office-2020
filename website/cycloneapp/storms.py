"""
Calculate the cyclones that pass through the radius of a point.
"""
import datetime
import json
import sys
import time
import geopy.distance

import pathlib

# Read a co-ordinate and radius.
# latitude = float(sys.argv[1])
# longitude = float(sys.argv[2])
# radius = float(sys.argv[3])
# input_file = sys.argv[4]

cyclone_nodes = []
nodes = 0
max_nodes = 10000000
input_file_path = "cycloneapp/static/globe/Real-Cyclones-Intense.csv"

print(f"Loading cyclone nodes from {input_file_path} into memory...")

with open(input_file_path, 'r') as file:
    for line in file:
        cyclone_nodes.append(line.strip().split(','))

        if nodes > max_nodes:
            print(f"WARNING: Cyclone nodes file has over {max_nodes} nodes. Only the first {max_nodes} will be read and used.")
            break

        nodes = nodes + 1

cyclone_nodes.pop(0)

print("Cyclone nodes loaded!")

query_id = 1

def storm_query_slow(latitude, longitude, radius, start_year, end_year):
    # Sorry for the globals Lewis xD
    global query_id, cyclone_nodes

    print(f"Query {query_id} received: {latitude} {longitude} {radius} {start_year} {end_year}")

    # Start timer.
    start = time.time()

    # Dictionary mapping cyclones to a list of their cyclone nodes
    print("Mapping cyclones to their cyclone nodes...")

    count = 0
    cyclones = {}
    cyclone = []
    last = cyclone_nodes[0][0]
    for node in cyclone_nodes:
        current = node[0]
        if current == last:
            cyclone.append([float(node[3]), float(node[4]), float(node[6])])
        else:
            cyclones[last] = cyclone
            cyclone = [[float(node[3]), float(node[4]), float(node[6])]]
            last = current

    mapping_end = time.time()
    seconds = round(mapping_end - start, 2)
    print(f"Time elapsed for mapping: {seconds} seconds")

    # Create a list of SIDs that have at least one node within boundaries
    print("Finding all cyclones that have at least one node within target boundary...")

    SIDs_in_radius = ['']
    for node in cyclone_nodes:
        year = datetime.date(int(node[5][:4]), 1, 1)
        # start_time = datetime.date(start_year, 1, 1)
        # end_time = datetime.date(end_year, 12, 31)
        coords_user = (latitude, longitude)
        coords_node = (node[3], node[4])
        distance = geopy.distance.distance(coords_user, coords_node).km
        # if distance < radius and start_time < year < end_time:
        #     if not node[0] == SIDs_in_radius[-1]:
        #         SIDs_in_radius.append(node[0])
        #         count = count + 1
        if distance < radius:
            if not node[0] == SIDs_in_radius[-1]:
                SIDs_in_radius.append(node[0])
                count = count + 1
    SIDs_in_radius.pop(0)

    boundaries_end = time.time()
    seconds = round(boundaries_end - mapping_end, 2)
    print(f"Time elapsed for boundary checking: {seconds} seconds")

    print("Filtering only valid cyclones...")

    # Filter the valid cyclones by SID and add to JSON
    filtered_cyclones = {}
    for SID in SIDs_in_radius:
        filtered_cyclones[SID] = cyclones[SID]

    filter_end = time.time()
    seconds = round(filter_end - boundaries_end, 2)
    print(f"Time elapsed for filtering: {seconds} seconds")

    # Output final performance results
    end = time.time()
    seconds = round(end - start, 2)
    print("Time elapsed:", seconds, "seconds")

    location = "(" + str(latitude) + ", " + str(longitude) + ")."
    print(f"{count} cyclones have at least one node within {radius} kilometres of {location}")
    
    print(f"Query {query_id} complete!")
    query_id += 1

    return filtered_cyclones

    # lines = json.dumps(filtered_cyclones, sort_keys=True, indent=4, separators=(',', ': '))
    # file = open('output.json', 'w')
    # file.truncate(0)
    # for line in lines:
    #     file.write(line)
    # file.close()