from collections import deque
from math import inf


def get_input():
    with open('18/input.txt', 'r') as i:
        input_lines = i.read().splitlines()
        x_lim, y_lim = len(input_lines[0]), len(input_lines)
        input_map = {k: v for (k, v) in
                     ((k, input_lines[k[1]][k[0]]) for k in list((x, y) for x in range(x_lim) for y in range(y_lim)))
                     if v != '#'}
    return input_map


def get_adj_points(coordinates):
    return ([
        (coordinates[0], coordinates[1] + 1),
        (coordinates[0], coordinates[1] - 1),
        (coordinates[0] + 1, coordinates[1]),
        (coordinates[0] - 1, coordinates[1])
    ])


def find_start(tunnel_map, char):
    for k, v in tunnel_map.items():
        if v == char:
            return k


def get_keys(tunnel_map):
    out = []
    for v in tunnel_map.values():
        if v.islower():
            out.append(v)
    return out


reachable_cache = {}


def get_reachable_keys(tunnel_map, start, owned_keys) -> dict:
    """return a dict with structure { key: (distance, (coordinates)) ,...}"""
    search = deque([start])
    dist_dict = {start: 0}
    keys = {}
    if owned_keys in reachable_cache:
        return reachable_cache[owned_keys]
    while len(search) > 0:
        curr_point = search.popleft()
        for point in get_adj_points(curr_point):
            if point in dist_dict:
                continue
            elif point in tunnel_map:
                point_type = tunnel_map[point]
                dist = dist_dict[curr_point] + 1
                dist_dict[point] = dist
                if point_type.isupper() and point_type.lower() not in owned_keys:
                    continue
                elif point_type.islower() and point_type not in owned_keys:
                    # key after key is 'not reachable'; only give directly reachable keys
                    keys[point_type] = (dist, point)
                search.append(point)
    reachable_cache[owned_keys] = keys
    return keys


def get_distances(tunnel_map, keys):
    all_dist_dict = {}
    for key in keys + ['@']:
        start = find_start(tunnel_map, key)
        search = deque([start])
        dist_dict = {start: 0}
        key_distances = {}
        while len(search) > 0:
            curr_point = search.popleft()
            for point in get_adj_points(curr_point):
                if point in dist_dict:
                    continue
                elif point in tunnel_map:
                    p = tunnel_map[point]
                    dist = dist_dict[curr_point] + 1;
                    dist_dict[point] = dist
                    if p.islower():
                        key_distances[p] = dist
                    search.append(point)
        all_dist_dict[key] = key_distances
    return all_dist_dict


def get_key_coords(tunnel_map, keys):
    d = {}
    for cord, char in tunnel_map.items():
        if char in keys:
            d[char] = cord
    return d


tunnel_map = get_input()
start = find_start(tunnel_map, '@')
keys = get_keys(tunnel_map)
key_cords = get_key_coords(tunnel_map, keys)
dist_dict = get_distances(tunnel_map, keys)


# seen_states = {}
# def traverse(tunnel_map, start, owned_keys, steps = 0, tot_steps = []):
#     '''Returns min distance from start to collect all keys'''

#     owned_keys = ''.join(sorted(owned_keys))

#     if (owned_keys, start) in seen_states.keys():
#         print(seen_states[owned_keys, start])
#         return seen_states[owned_keys, start]

#     reachable_keys = get_reachable_keys(tunnel_map, start, owned_keys)
#     if len(reachable_keys) == 0: #min dist to collect all = 0, already have all
#         return 0
#     else:
#         route_lens = []
#         for key in reachable_keys.keys():
#             dist, start = reachable_keys[key]
#             # print(key, owned_keys)
#             route_lens.append(dist + traverse(tunnel_map, start, owned_keys + key,steps + dist, tot_steps))
#         min_steps = min(route_lens)
#         seen_states[owned_keys, start] = min_steps
#     return min_steps
#     return tot_steps

def distance_to_collect(tunnel_map, start, owned_keys, cache= {}):
    """Perform BFS with updating available keys"""

    start_key = tunnel_map[start]
    owned_keys = ''.join(sorted(owned_keys))

    if (start, owned_keys) in cache:
        return cache[(start, owned_keys)]

    reachable_keys = get_reachable_keys(tunnel_map, start, owned_keys).keys()
    if len(reachable_keys) == 0:
        return 0

    res = inf
    for key in reachable_keys:
        distance, position = dist_dict[start_key][key], key_cords[key]
        d = (distance + distance_to_collect(tunnel_map, position, owned_keys + key, cache))
        res = min(res, d)
    cache[start, owned_keys] = res
    return res


print(distance_to_collect(tunnel_map, start, ''))

# want to pre_sort reachable keys based on owned_keys and state, as well as do dist map irrespective of distances
# Parse map into just walkable space

# Cache each state of reachable keys
# Go through and use Fibbonacci search (see if cached, if not, get and cache)
# Djikstra would be v complex due to each key changing the network, recursive BFS seems easier
