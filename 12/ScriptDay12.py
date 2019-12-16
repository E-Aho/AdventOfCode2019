import re
from itertools import combinations
from math import gcd

def get_input():
    with open('12/input.txt', 'r') as input_file:
        return input_file.readlines()

def get_starting_coordinates():
    pattern = re.compile("=([-\d]*)[,>]")
    coordinate_list = []
    for line in get_input():
        coordinate_list.append(list(map(int,re.findall(pattern, line))))
    return coordinate_list

class Moon:
    def __init__(self, coordinates, v):
        self.coordinates = coordinates
        self.v = v
        
    def apply_vel(self):
        for i in range(3):
            self.coordinates[i] += self.v[i]

def adjust_vels(moon1, moon2):
    for i in range(3):
        if moon1.coordinates[i] == moon2.coordinates[i]:
            pass
        elif moon1.coordinates[i] > moon2.coordinates[i]:
            moon1.v[i] -= 1; moon2.v[i] += 1 
        elif moon1.coordinates[i] < moon2.coordinates[i]:
            moon1.v[i] += 1; moon2.v[i] -= 1

def adjust_single_vel(moon1, moon2, i):
    if moon1.coordinates[i] == moon2.coordinates[i]:
        pass
    elif moon1.coordinates[i] > moon2.coordinates[i]:
        moon1.v[i] -= 1; moon2.v[i] += 1 
    elif moon1.coordinates[i] < moon2.coordinates[i]:
        moon1.v[i] += 1 ; moon2.v[i] -= 1

def get_GPE(moon):    
    return (sum(abs(moon.coordinates[i]) for i in range(3)))

def get_KE(moon):
    return (sum(abs(moon.v[i]) for i in range(3)))

def get_TE(moon):
    return (get_GPE(moon) * get_KE(moon))

def are_stationary(moons, axis):
    for moon in moons:
        if moon.v[axis] != 0:
            return False
        return True

def get_moons(coordinate_list):
    return [Moon(cords, [0,0,0]) for cords in coordinate_list]

#Part 1
moons = get_moons(get_starting_coordinates())
for step in range(1,1001):
    moon_pairs = combinations(moons,2)
    for pair in moon_pairs:
        adjust_vels(pair[0], pair[1])
    for moon in moons:
        moon.apply_vel()

sys_energy = sum(get_TE(moon) for moon in moons)
print('\nPart 1: \nTotal energy of system after 1000 steps:', sys_energy, '\n')

#Part 2
#Each axis is independent, so we can find the cycle length for each axis and get the LCM for these cycle lengths

def get_lcm(num_list):
    lcm = num_list[0]
    for num in num_list[1:]:
        lcm = int(lcm*num/gcd(lcm, num))
    return lcm

def get_cycle_length(axis, moons): #Gets number of steps until all planets returns to starting position in a given axis
    step = 0
    original_pos= list(map(int,[cords[i] for cords in get_starting_coordinates()]))
    while True:
        step += 1
        moon_pairs = combinations(moons,2)
        for pair in moon_pairs:
            adjust_single_vel(pair[0], pair[1],axis)
        for moon in moons:
            moon.apply_vel()
        if are_stationary(moons, axis):
            if [moon.coordinates[axis] for moon in moons] == original_pos:
                return step

axis_cycles = []
print('Part 2:\n')
for i in range(3): #find time for each axis to cycle
    print('Running axis number: ', i+1)
    moons = get_moons(get_starting_coordinates())
    cycle_len = get_cycle_length(i,moons)
    axis_cycles.append(cycle_len)
    print('Axis {0} has length: {1}\n'.format(i+1,cycle_len))

print('Number of steps to return to start: ', get_lcm(axis_cycles))
