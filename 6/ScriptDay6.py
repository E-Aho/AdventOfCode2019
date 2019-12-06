import math
import time

class node:
    def __init__(self, name:str, children:list, parent:list):
        self.name = name
        self.children = children
        self.parent = parent

def parse_input(input_map):

    planet_dict = {}
    for line in input_map.splitlines():
        (parent, child) = line.split(')')
        if parent in planet_dict:
            planet_dict[parent].children.append(child)
        else:
            planet_dict[parent] = node(parent,[child],[])

        if child in planet_dict:
            planet_dict[child].parent.append(parent)
        else:
            planet_dict[child] = node(child,[],[parent])
    return planet_dict

def get_tot_orbits(starting_node:node, planet_dict:dict, starting_depth: int):

    tot_connectivity = 0
    curr_depth = starting_depth + 1
    for child in starting_node.children:
        new_node = planet_dict[child]
        tot_connectivity += curr_depth #direct + indirect orbits for this planet
        tot_connectivity += get_tot_orbits(new_node,planet_dict,curr_depth) #direct + indirect orbits for children of this planet
    return tot_connectivity

def dijkstra_search(start, target, planet_dict):

    unvisited_nodes = set(planet_dict.keys())
    u = planet_dict[start]

    min_distances = {}
    for node in unvisited_nodes:
        min_distances[node] = math.inf

    min_distances[u.name] = 0

    while len(unvisited_nodes) > 0 and target in unvisited_nodes:

        tempDist = math.inf
        for v in unvisited_nodes:
            if min_distances[v] <= tempDist:
                tempDist = min_distances[v]
                curr_node = v
        
        unvisited_nodes.remove(curr_node)

        for node in (planet_dict[curr_node].children + planet_dict[curr_node].parent):
            new_dist = min_distances[curr_node] + 1
            if new_dist < min_distances[node]:
                min_distances[node] = new_dist
                
    return(min_distances[target])

#Run functions and output solutions
with open('6/input.txt', 'r') as input_file:
    raw_map = input_file.read()
    planet_dict = parse_input(raw_map)

#Part 1 solution
start_1 = time.time()
CoM = planet_dict['COM']
tot_orbits = get_tot_orbits(CoM, planet_dict, 0)
end_1 = time.time()
print('\nPart 1: \nTotal orbits: ', tot_orbits)
print('Time to complete part 1: %.4fs\n' % (end_1-start_1))

#Part 2 solution
start_2 = time.time()
distance = dijkstra_search('YOU', 'SAN', planet_dict)
end_2 = time.time()
print("\nPart 2: \nDistance from you to Santa: ", distance-2) #-2, we don't care about journey from you to your orbit and SAN to theirs
print('Time to complete part 2: %.4fs\n' % (end_2-start_2))
print('Total time to complete both parts: %.4fs\n' % (end_2-start_1))


