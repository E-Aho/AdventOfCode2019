import time

print('\nRunning Day 3 Script\n')
start_time = time.time()


def parse_instruction(instruction):  # returns a vector
    (direction, magnitude) = (instruction[0], int(instruction[1:]))
    if direction == "R":
        return magnitude, 0
    elif direction == "L":
        return -magnitude, 0
    elif direction == "U":
        return 0, magnitude
    elif direction == "D":
        return 0, -magnitude
    else:
        print('Error parsing instruction: ', instruction)
        return 0, 0


def get_origin():  # Could be done with deep copy instead of function
    return 0, 0


def get_manhattan(x, y):
    return abs(x) + abs(y)


def add_segment(start_pos, vector):
    return start_pos[0] + vector[0], start_pos[1] + vector[1]


def check_intersect(a, b):
    # Compare x value of y segment with range of x values for x segment, and repeat for y of x segment.
    # If both within each other segment's ranges, intersection is at x val of y segment and y val of x segment
    if a[0][1] == a[1][1]:
        x_seg = a
        y_seg = b
    else:
        x_seg = b
        y_seg = a
    if min(x_seg[0][0], x_seg[1][0]) <= y_seg[0][0] <= max(x_seg[0][0], x_seg[1][0]):
        if min(y_seg[0][1], y_seg[1][1]) <= x_seg[0][1] <= max(y_seg[0][1], y_seg[1][1]):
            return y_seg[0][0], x_seg[0][1]  # coordinates of intersection
        else:
            return None
    else:
        return None


def get_instructions(inp):
    wires_instructions = []  # will contain the parsed input
    for wire in inp:
        instructions = wire.split(',')
        new_wire = list(map(parse_instruction, instructions))
        wires_instructions.append(new_wire)
    return wires_instructions


def get_maps(instructions):
    maps = []
    for wire in instructions:
        start = (0, 0)
        wire_map = []
        for segment_direction in wire:
            end = add_segment(start, segment_direction)
            wire_map.append((start, end))
            start = end
        maps.append(wire_map)
    return maps


def get_distances_to_intersections(maps):
    intersections = []
    for a in maps[0]:
        for b in maps[1]:
            intersect = check_intersect(a, b)
            if intersect is not None:
                intersections.append(intersect)

    dist = []
    for intersect in intersections:
        man_dist = get_manhattan(intersect[0], intersect[1])
        if man_dist > 0:
            dist.append(man_dist)
    return dist


def get_stepped_maps(instructions):
    maps = []
    for w in instructions:
        start = (0, 0)
        stepped_map = []
        tot_length = 0  # length to start of segment
        for segment_direction in w:
            end = add_segment(start, segment_direction)
            stepped_map.append((start, end, tot_length))
            tot_length += (abs(segment_direction[0]) + abs(segment_direction[1]))
            start = end
        maps.append(stepped_map)
    return maps


def get_steps(point_1, point_2):
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])


def get_steps_to_intersections(maps):
    steps_to_intersections = []
    for a in maps[0]:
        for b in maps[1]:
            intersect = check_intersect(a, b)
            if intersect:
                a_steps = get_steps(a[0], intersect)
                b_steps = get_steps(b[0], intersect)
                tot_steps = a[2] + b[2] + a_steps + b_steps
                if tot_steps != 0:
                    steps_to_intersections.append(tot_steps)
    return steps_to_intersections


if __name__ == '__main__':
    with open('03/input.txt', 'r') as input_file:
        raw_wires = input_file.readlines()
        wire_instructions = get_instructions(raw_wires)
        wire_maps = get_maps(wire_instructions)
        stepped_maps = get_stepped_maps(wire_instructions)

    start_time = time.time()
    distances = get_distances_to_intersections(wire_maps)
    print("\nPart 1: \nMinimum manhattan distance to an intersection: ", min(distances))

    min_steps = min(get_steps_to_intersections(stepped_maps))
    print('\nPart 2: \nMinimum steps to intersections:', min_steps)
    end_time = time.time()
    print('\nTotal time to complete: %.4fs' % (end_time - start_time))
