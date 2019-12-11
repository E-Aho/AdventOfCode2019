from IntcodeMethods import opcode_comp
from collections import defaultdict
import operator

with open('11/input.txt','r') as input_file:
    initial_state = input_file.read().split(',')

def rotate(dir,val): #0 -> turn left(counterclockwise), 1 -> turn right(clockwise)
    if val == 0:
        return(-dir[1], dir[0])
    elif val == 1:
        return(dir[1], -dir[0])

class paint_robot:
    def __init__(self):
        self.computer = opcode_comp(initial_state)
        self.position = (0,0) #position is x,y cartesian coord
        self.direction = (0,1) # dir is unit cartesian vector
        self.been_painted = set({}) #needed because of how defaultdict handles looking at dict as creating a val
        self.map = defaultdict(int)

    def do_rot(self, val):
        self.direction = rotate(self.direction, val)
    
    def do_move(self):
        new_pos = tuple(map(operator.add, self.position, self.direction))
        self.position = new_pos

    def check_panel(self):
        return self.map[self.position]

    def paint_panel(self, colour): #add position to dict and paint it
        self.map[self.position] = colour

    def run_paint(self):
        while True:
            #check for input, then paint
            self.computer.add_input(self.check_panel())
            self.computer.run()
            if self.computer.finished is True:
                break
            paint_colour = self.computer.get_output()
            self.paint_panel(paint_colour)
            if self.position not in self.been_painted: 
                self.been_painted.add(self.position)

            #rotate and move
            self.computer.run()
            direction = self.computer.get_output()
            self.do_rot(direction)
            self.do_move()

#Part 1
robot = paint_robot() 
robot.run_paint()
print('\nNumber of unique panels painted: ', len(robot.been_painted))

#Part 2
robot2 = paint_robot()
robot2.map[(0,0)] = 1
robot2.run_paint()

xr, yr = zip(*(robot2.map.keys()))
min_x, max_x, min_y, max_y = min(xr), max(xr), min(yr), max(yr)

output = '\n'
for j in range(max_y, min_y-1, -1):
    for i in range(min_x, max_x, 1):
        if robot2.map[(i,j)] == 1:
            output += ('█')
        else:
            output += ('░')
    output += ('\n')

print('\nCode for part 2: \n',output)
