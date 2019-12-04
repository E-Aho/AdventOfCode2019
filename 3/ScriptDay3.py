with open('3/input.txt', 'r') as input_file:
    raw_wires = input_file.readlines()

def parse_instruction(instruction): #returns a vector
    (direction, magnitude) = (instruction[0], int(instruction[1:]))
    if direction == "R":
        return(magnitude, 0)
    elif direction == "L":
        return(-magnitude, 0)
    elif direction == "U":
        return(0, magnitude)
    elif direction == "D":
        return(0, -magnitude)
    else:
        print('Error parsing instruction: ', instruction)
        return(0,0)

def get_origin():
    return (0,0)

def get_manhattan(x,y):
    return(abs(x) + abs(y))

def add_segment(start, vector):
    return (start[0] + vector[0], start[1] + vector[1])

def check_intersect(a,b):
    if(a[0][1] == a[1][1]):
        x_seg = a
        y_seg = b
    else:
        x_seg = b
        y_seg = a
    if(min(x_seg[0][0], x_seg[1][0]) <= y_seg[0][0] <= max(x_seg[0][0], x_seg[1][0])):
        if(min(y_seg[0][1], y_seg[1][1]) <= x_seg[0][1] <= max(y_seg[0][1], y_seg[1][1])):
            return(y_seg[0][0], x_seg[0][1])
        else:
            return False
    else:
        return False

def get_stepped_maps(wire_instructions):
    maps = []
    for wire in wires_instructions:
        start = get_origin()
        wire_map = []
        tot_length = 0 #length to start of segment
        for segment_direction in wire:
            end = add_segment(start,segment_direction)
            wire_map.append((start,end,tot_length))
            tot_length += (abs(segment_direction[0]) + abs(segment_direction[1]))
            start = end
        maps.append(wire_map)
    return maps

wires_instructions = []

for wire in raw_wires:
    instructions = wire.split(',')
    new_wire = list(map(parse_instruction, instructions))
    wires_instructions.append(new_wire)

wire_maps = []


for wire in wires_instructions:
    start = get_origin()
    wire_map = []
    for segment_direction in wire:
        end = add_segment(start,segment_direction)
        wire_map.append((start,end))
        start = end
    wire_maps.append(wire_map)


intersections = []

for a in wire_maps[0]:
    for b in wire_maps[1]:
        res = check_intersect(a,b)
        if res != False:
            intersections.append(res)

dist = []

for intersect in intersections:
    man_dist = get_manhattan(intersect[0], intersect[1])
    if man_dist > 0:
        dist.append(man_dist)

print("Minimum manhattan distance to an intersection: ", min(dist))




stepped_maps = get_stepped_maps(wires_instructions)

def get_steps(point_1, point_2):
    return(abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1]))

steps_to_intersections = []

for a in stepped_maps[0]:
    for b in stepped_maps[1]:
        res = check_intersect(a,b)
        if res != False:
            intersection = res
            a_steps = get_steps(a[0], intersection)
            b_steps = get_steps(b[0], intersection)
            tot_steps = a[2] + b[2] + a_steps + b_steps
            if tot_steps != 0:
                steps_to_intersections.append(tot_steps)

print('Minimum steps to intersections:' , min(steps_to_intersections)) # [1:] needed here to discount intersection where 
