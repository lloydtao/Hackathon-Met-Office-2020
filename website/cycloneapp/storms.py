"""
Calculate the cyclones that pass through the radius of a point.
"""
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

def storm_query_slow(latitude, longitude, radius, input_file):
    # Populate cyclone nodes.
    nodes = 0
    # max_nodes = 10000
    max_nodes = 10000000
    cyclone_nodes = []
    
    print(pathlib.Path().absolute())

    file = open(input_file, 'r')
    for line in file:
        cyclone_nodes.append(line.strip().split(','))
        if nodes > max_nodes:
            print("WARNING: Input has over", max_nodes, "nodes. Only read first", max_nodes, "cyclone nodes.")
            break
        nodes = nodes + 1
    cyclone_nodes.pop(0)

    # Dictionary mapping cyclones to a list of their cyclone nodes.
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

    # Start timer.
    start = time.time()

    # Create a list of SIDs that have at least one node within boundaries.
    SIDs_in_radius = ['']
    for node in cyclone_nodes:
        coords_user = (latitude, longitude)
        coords_node = (node[3], node[4])
        distance = geopy.distance.distance(coords_user, coords_node).km
        if distance < radius:
            if not node[0] == SIDs_in_radius[-1]:
                SIDs_in_radius.append(node[0])
                count = count + 1
    SIDs_in_radius.pop(0)

    # Filter the valid cyclones by SID and add to JSON.
    filtered_cyclones = {}
    for SID in SIDs_in_radius:
        filtered_cyclones[SID] = cyclones[SID]

    return filtered_cyclones
    # lines = json.dumps(filtered_cyclones, sort_keys=True, indent=4, separators=(',', ': '))
    # file = open('output.json', 'w')
    # file.truncate(0)
    # for line in lines:
    #     file.write(line)
    # file.close()

    # End timer.
    # end = time.time()
    # seconds = round(end - start, 2)
    # print("Time elapsed:", seconds, "seconds")

    # location = "(" + str(latitude) + ", " + str(longitude) + ")."
    # print(count, "cyclones have at least one node within", radius, "kilometres of", location)