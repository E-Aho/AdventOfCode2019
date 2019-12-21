from math import pi, atan2
from collections import defaultdict


def get_angle(x, y):
    return round(((atan2(x, -y) + 2 * pi) % (2 * pi)), 10)  # Uses weird -y here because of odd axis sys


def get_input(file_loc):
    with open(file_loc, 'r') as input_file:
        asteroids_raw = input_file.read().splitlines()
    return [Asteroid(Cords(x, y)) for y, line in enumerate(asteroids_raw) for x, char in enumerate(line) if char == '#']


class Cords:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Asteroid:
    def __init__(self, cords):
        self.cords = cords
        self.x = cords.x
        self.y = cords.y
        self.los_dict = defaultdict(list)


def check_los(origin: Asteroid, asteroids: list):
    for asteroid in asteroids:
        rel_cords = Cords(asteroid.x - origin.x, asteroid.y - origin.y)
        direction = get_angle(rel_cords.x, rel_cords.y)
        origin.los_dict[direction].append(asteroid)


def find_station(asteroids):
    """"returns the count LOS for the station, and the station as an Asteroid object"""
    max_los = 0
    position = None

    for i in range(len(asteroids)):
        origin = asteroids[i]
        others = asteroids[:i] + asteroids[i + 1:]
        check_los(origin, others)
        if len(origin.los_dict) > max_los:
            max_los = len(origin.los_dict)
            position = origin

    return max_los, position


# For Part 2


def dist_from_origin(asteroid):
    return (asteroid.x - station.x) ** 2 + (asteroid.y - station.y) ** 2


def lazer(origin, zap_order, zap_lim):
    zap_count = 0
    while True:
        for direction in zap_order:
            if len(origin.los_dict[direction]) > 0:
                zap_count += 1
                origin.los_dict[direction].sort(key=dist_from_origin)
                zapped = origin.los_dict[direction].pop(0)
                if zap_count == zap_lim:
                    return zapped  # * 100 + zapped.y


if __name__ == "__main__":
    asteroid_array = get_input('10/input.txt')
    max_visible, station = find_station(asteroid_array)
    print(f'Part 1:\nLargest number of visible asteroids: {max_visible}\n')  # 286
    sweep_order = sorted(list(station.los_dict.keys()))  # keys are angle from station's y axis clockwise
    final_zap = lazer(station, sweep_order, 200)
    print(f'Part 2:\n200th asteroid has coordinates: {final_zap.x}, {final_zap.y}')  # 5, 4
    print(f'Solution to part 2: {final_zap.x * 100 + final_zap.y}')  # 504
