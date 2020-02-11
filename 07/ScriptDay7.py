from itertools import permutations
from math import inf

from Methods import OpcodeComp


def get_initial_state():
    with open('07/input.txt', 'r') as input_file:
        return tuple(map(int, input_file.read().split(',')))


def part_1():
    max_out = 0
    perms = permutations(range(count_amps))

    for perm in perms:
        output = 0
        for phase in perm:
            processor = OpcodeComp(initial_array)
            processor.phase = phase
            processor.input = output
            processor.run_opcode()
            output = processor.get_output()
        if output > max_out:
            max_out = output
    return max_out


class SetupAmps:
    def __init__(self, initial_state, sequence):
        self.memory = list(initial_state)
        self.sequence = sequence
        self.count_amps = 5
        self.final_amp = self.count_amps - 1
        self.amps = [OpcodeComp(self.memory) for _ in range(self.count_amps)]
        self.set_sequence(sequence)

    def set_sequence(self, sequence):
        for i in range(self.count_amps):
            self.amps[i].set_phase(sequence[i])

    def run(self):
        a = self.amps[0]
        e = self.amps[-1]
        e.set_output(0)  # sets input for first run on A to be 0
        index = 0

        while True:
            current_amp = self.amps[index]
            last_amp = self.amps[index - 1]
            current_amp.set_input(last_amp.get_output())
            current_amp.run_opcode()

            if current_amp.has_finished():
                break
            else:
                index += 1
                if index > self.final_amp:
                    index = 0

    def get_output(self):
        return self.amps[-1].get_output()


def part_2():
    perms = permutations(range(5, 10))
    max_out = -inf

    for perm in perms:
        setup = SetupAmps(initial_array, perm)
        setup.run()
        output = setup.get_output()
        if output > max_out:
            max_out = output
    return max_out


if __name__ == "__main__":
    count_amps = 5
    initial_array = get_initial_state()

    print('Part 1:\nMaximum output: ', part_1())
    print('Part 1:\nMaximum output: ', part_2())
