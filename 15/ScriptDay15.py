from IntcodeMethods import opcode_comp
from math import inf

with open('15/input.txt', 'r') as input_file:
        initial_state = tuple(map(int,input_file.read().split(',')))

input_to_dir = {
    1:(0,1),
    2:(0,-1),
    3:(-1,0),
    4:(1,0)
}

dir_to_input = {
    (0,1):1,
    (0,-1):2,
    (-1,0):3,
    (1,0):4
}

def to_right(dir):
    return((dir[1], -dir[0]))

def to_left(dir):
    return((-dir[1], dir[0]))

def add_vec(vec1, vec2):
    return((vec1[0] + vec2[0], vec1[1] + vec2[1]))

class Droid:
    def __init__(self):
        self.computer = opcode_comp(initial_state)
        self.map = {(0,0):'X'}
        self.position = (0,0)
        self.input_val = 0
        self.dir = (1,0)
        self.dist = 0
        self.dist_map = {(0,0):0}
        self.oxy_loc = None
        self.oxy_map = {}
        self.oxy_dist = inf
        
        
    def get_input(self):
        self.input_val = 0
        while True:
            next_in = int(input('Please enter an integer'))
            if next_in in [1,2,3,4]:
                self.input_val = (next_in)
                self.computer.set_input(self.input_val)
                break
            else:
                print('Invalid input: enter a number 1-4 inclusive')
    
    def read_output(self, output):
        direction = self.dir
        new_pos = add_vec(self.position, direction)
        if output == 0:
            self.map[new_pos] ='▊'
        elif output == 1:
            self.position = new_pos
            self.map[new_pos] = ' '
            self.dist += 1
            self.oxy_dist += 1
        elif output == 2:
            self.position = new_pos
            self.map[new_pos] = '%'
            self.dist += 1
            self.oxy_dist += 1

            self.oxy_dist = 0
            self.oxy_loc = new_pos

    def print_map(self):
        out = '\n'
        xr, yr = zip(*(self.map.keys()))
        min_x, max_x, min_y, max_y = min(xr), max(xr), min(yr), max(yr)
        for j in range(min_y-1, max_y+1, 1):
            for i in range(-30, 30, 1):
                if self.position == (i,j):
                    out += 'D'
                else:
                    out += self.map.get((i,j),'▒')
            out += '\n'
        print(out)
    
    def do_dist(self):
        if self.position in self.dist_map:
            if self.dist_map[self.position] < self.dist:
                self.dist = self.dist_map[self.position]
            elif self.dist_map[self.position] > self.dist:
                self.dist_map[self.position] = self.dist
        else:
            self.dist_map[self.position] = self.dist
        

    def auto_input(self):
        if self.computer.output == 0:
            self.dir = to_right(self.dir)
        elif self.computer.output == 1:
            self.dir = to_left(self.dir)
        elif self.computer.output == 2:
            self.dir = to_left(self.dir)
        self.computer.set_input(dir_to_input[self.dir])

    def do_ox_diffuse(self):
        if self.position in self.oxy_map:
            if self.oxy_map[self.position] < self.oxy_dist:
                self.oxy_dist = self.oxy_map[self.position]
            elif self.oxy_dist < self.oxy_map[self.position]:
                self.oxy_map[self.position] = self.oxy_dist
        else:
            self.oxy_map[self.position] = self.oxy_dist
        

    def run_droid(self):
        while True:
            self.get_input()
            print(self.input_val, self.computer.inputs)
            self.computer.run()
            out = self.computer.output
            self.read_output(out)
            self.print_map()

    def auto_run(self):
        i = 0
        while i < 10000:
            self.auto_input()
            self.computer.run()
            out = self.computer.output
            self.read_output(out)
            self.print_map()
            self.do_dist()
            if self.oxy_loc is not None:
                self.do_ox_diffuse()
            i += 1

        print(self.dist_map.get(self.oxy_loc, 0))
        print(max(self.oxy_map.values()))



        
droid = Droid()

droid.auto_run()
