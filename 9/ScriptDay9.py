from IntcodeMethods import opcode_comp


def get_initial_state():
    with open('9/input.txt', 'r') as input_file:
        return(tuple(map(int, input_file.read().split(','))))

initial_array = get_initial_state()

processor = opcode_comp(initial_array)
processor.add_input(1)
print('\nRunning part 1:')
processor.run()

processor = opcode_comp(initial_array)
processor.add_input(2)
print('\nRunning part 2')
processor.run()
