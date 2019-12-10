from math import pi, atan2
from collections import defaultdict

class cords:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class asteroid:
    def __init__(self, cords):
        self.cords = cords
        self.x = cords.x
        self.y = cords.y
        self.los_dict = defaultdict(list)

def check_los(origin:asteroid, asteroids:list):
    for asteroid in asteroids:
        rel_cords = cords(asteroid.x - origin.x, asteroid.y - origin.y)
        direction = get_angle(rel_cords.x, rel_cords.y)
        origin.los_dict[direction].append(asteroid)

def get_input():
    with open('10/input.txt', 'r') as input_file:
        return input_file.read().splitlines()

asteroid_map = get_input()
asteroids = [asteroid(cords(x,y)) for y, line in enumerate(asteroid_map) for x,char in enumerate(line) if char == '#']

def get_angle(x,y):
    return (round(((atan2(x,-y)+ 2*pi) % (2*pi)),10)) #Uses weird -y here because of odd axis sys

max_los = 0
for i in range(len(asteroids)):
    origin = asteroids[i]
    others = asteroids[:i] + asteroids[i+1:]
    check_los(origin, others)
    if len(origin.los_dict) > max_los:
        max_los = len(origin.los_dict)
        station = origin

print('The max count of asteroids in LOS:', max_los)

def dist_from_origin(asteroid):
    return ((asteroid.x - station.x)**2 + (asteroid.y-station.y)**2)

# print(station.los_dict.keys())
sweep_order = sorted(list(station.los_dict.keys()))

def lazer(origin, zap_order):
    zap_count = 0
    while True:
        for direction in zap_order:
            if len(origin.los_dict[direction]) > 0:
                zap_count += 1
                origin.los_dict[direction].sort(key=dist_from_origin)
                zapped = origin.los_dict[direction].pop(0)
                if zap_count == 200:
                    return zapped.x*100+zapped.y


print(lazer(station,sweep_order))