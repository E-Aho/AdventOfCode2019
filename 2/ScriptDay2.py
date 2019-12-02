
def get_initial_state(): #could do with deep copy instead of fetching each time
    with open('2/input.txt', 'r') as input_file:
        return(list(map(int, input_file.read().split(','))))
    
def perform_action(array, index):
    (Opcode, pos1, pos2, pos3) = array[index:index+4]
    if Opcode == 1:
        array[pos3] = array[pos1] + array[pos2]
        return False #should not halt
    elif Opcode == 2:
        array[pos3] = array[pos1] * array[pos2]
        return False #should not halt
    elif Opcode == 99:
        return True #should halt
    else: 
        return True #encountered error

intcode = get_initial_state()
intcode[1] = 12
intcode[2] = 2

def run_intcode(intcode_arr):
    i = 0
    while i < len(intcode_arr):
        if perform_action(intcode_arr, i): #true in case of Opcode 99
            break
        else:
            i += 4
    return intcode_arr

print('Output for first task:', (run_intcode(intcode))[0])

target_output = 19690720

print('\nSearching for Noun + Verb combinations... \n')
for noun in range(100):
    for verb in range(100):
        memory = get_initial_state()
        memory[1] = noun
        memory[2] = verb
        if run_intcode(memory)[0] == target_output:
            print('Success! Noun * 100 + Verb ==', (noun*100 + verb))
        