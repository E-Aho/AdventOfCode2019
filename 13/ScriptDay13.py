from IntcodeMethods import opcode_comp

class Tile:
    def __init__(self, id:int):
        self.id = int(id)
        
    def get_image(self):
        if self.id == 0:
            return(' ') #Empty space
        elif self.id == 1:
            return('▊') #Wall
        elif self.id == 2:
            return('▒') #Block
        elif self.id == 3:
            return('═') #Horizontal paddle
        elif self.id == 4:
            return('o') #Ball
        else:
            print('err')

class Game():
    def __init__(self):
        self.map = {}
        self.computer = opcode_comp(list(initial_state))
        self.score = int
        self.ball_x = -1
        self.paddle_x = -1

    def set_map(self): #read opcode instructions to generate current map state and score
        instructions = []
        while True: 
            if len(instructions) < 3:
                self.computer.run()
                if self.computer.finished is True:
                    break
                instructions.append(self.computer.get_output())
            if len(instructions) == 3:
                x, y, i = tuple(map(int, instructions))
                if (x == -1) and (y == 0): 
                    self.score = i
                else:
                    if i == 3: #paddle position
                        self.paddle_x = x
                        self.computer.set_input(self.get_auto_input())
                    elif i == 4: #ball position
                        self.ball_x = x
                        self.computer.set_input(self.get_auto_input())
                    self.map[(x, y)] = Tile(i)
                instructions = []

    def print_map(self): #print current map state to terminal
        out = '\n'
        xr, yr = zip(*(self.map.keys()))
        min_x, max_x, min_y, max_y = min(xr), max(xr), min(yr), max(yr)
        for j in range(min_y-1, max_y, 1):
            for i in range(min_x, max_x+1, 1):
                out += (self.map.get((i,j),Tile(0))).get_image()
            out += '\n'
        print(out)
    
    def get_count(self, tile_id): #return number of a given tile type on map
        count = 0
        for tile in self.map.values():
            if tile.id == tile_id:
                count += 1
        return count

    def get_auto_input(self): #get direction as integer paddle should move
        if self.ball_x == self.paddle_x:
            return 0
        elif self.ball_x < self.paddle_x:
            return -1
        elif self.ball_x > self.paddle_x:
            return 1

    def auto_run_game(self): #control paddle automatically, run game and win
        print('Running auto game...')
        count_ball = 1; count_block = 1 #arbitrary number > 0
        while (count_ball  > 0) and (count_block > 0):
            inp = self.get_auto_input()
            self.computer.set_input(self.get_auto_input())
            self.set_map()
            count_ball = self.get_count(4)
            count_block = self.get_count(2)
        print('Game is finished! Score: ', self.score)

def main():
    
    #Part 1
    print('\nPart 1:')
    screen = Game(); screen.set_map(); screen.print_map()
    print('The number of blocks in the screen is:', screen.get_count(2))

    #Part 2
    print('\nPart 2:')
    game = Game();
    game.computer.memory[0] = 2 #'Set to free play'
    game.auto_run_game()

if __name__ == "__main__":
    with open('13/input.txt', 'r') as input_file:
        initial_state = tuple(map(int,input_file.read().split(',')))
        
    main()