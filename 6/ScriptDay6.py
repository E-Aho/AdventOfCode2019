import math
import time


class Node:
    def __init__(self, name: str, children: list, parent: list):
        self.name = name
        self.children = children
        self.parent = parent


def parse_input(input_map):
    planets = {}
    for line in input_map.splitlines():
        (parent, child) = line.split(')')
        if parent in planets:
            planets[parent].children.append(child)
        else:
            planets[parent] = Node(parent, [child], [])

        if child in planets:
            planets[child].parent.append(parent)
        else:
            planets[child] = Node(child, [], [parent])
    return planets


def get_tot_orbits(starting_node: Node, planets: dict, starting_depth: int):
    tot_connectivity = 0
    curr_depth = starting_depth + 1
    for child in starting_node.children:
        new_node = planets[child]
        tot_connectivity += curr_depth  # direct + indirect orbits for this planet
        tot_connectivity += get_tot_orbits(new_node, planets,
                                           curr_depth)  # direct + indirect orbits for children of this planet
    return tot_connectivity


def graph_search(start, target, planets):  # pseudo dijkstra search.
    # More complex than need be for this problem but may be handy in a later problem if graph not a tree

    unvisited_nodes = set(planets.keys())
    u = planets[start]
    curr_node = u

    min_distances = {}
    for n in unvisited_nodes:
        min_distances[n] = math.inf

    min_distances[u.name] = 0

    while len(unvisited_nodes) > 0 and target in unvisited_nodes:

        temp_dist = math.inf
        for v in unvisited_nodes:
            if min_distances[v] <= temp_dist:
                temp_dist = min_distances[v]
                curr_node = v

        unvisited_nodes.remove(curr_node)

        for n in (planets[curr_node].children + planets[curr_node].parent):
            new_dist = min_distances[curr_node] + 1
            if new_dist < min_distances[n]:
                min_distances[n] = new_dist

    return min_distances[target]


# Run functions and output solutions
with open('6/input.txt', 'r') as input_file:
    raw_map = input_file.read()
    planet_dict = parse_input(raw_map)

if __name__ == "__main__":

    start_1 = time.time()
    CoM = planet_dict['COM']
    tot_orbits = get_tot_orbits(CoM, planet_dict, 0)
    end_1 = time.time()
    print('\nPart 1: \nTotal orbits: ', tot_orbits)
    print('Time to complete part 1: %.4fs\n' % (end_1 - start_1))

    start_2 = time.time()
    distance = graph_search('YOU', 'SAN', planet_dict)
    end_2 = time.time()
    print("\nPart 2: \nDistance from you to Santa: ", distance - 2)  # -2, we don't SAN or you to orbits
    print('Time to complete part 2: %.4fs\n' % (end_2 - start_2))
    print('Total time to complete both parts: %.4fs\n' % (end_2 - start_1))
