def opcode_1(array, modes, index):
    params = get_params(array, modes, index)
    array[(array[index + 3])] = params[1] + params[0]


def opcode_2(array, modes, index):
    params = get_params(array, modes, index)
    array[(array[index + 3])] = params[1] * params[0]


def opcode_3(array, index, input_val):
    address = array[index + 1]
    array[address] = input_val


def opcode_4(array, index):
    address = int(array[index + 1])
    return int(array[address])


def opcode_5(array, modes, index):
    params = get_params(array, modes, index)
    if params[0] != 0:
        return params[1]
    else:
        return index


def opcode_6(array, modes, index):
    params = get_params(array, modes, index)
    if params[0] == 0:
        return params[1]
    else:
        return index


def opcode_7(array, modes, index):
    params = get_params(array, modes, index)
    if params[0] < params[1]:
        array[array[index + 3]] = 1
    else:
        array[array[index + 3]] = 0


def opcode_8(array, modes, index):
    params = get_params(array, modes, index)
    if params[0] == params[1]:
        array[array[index + 3]] = 1
    else:
        array[array[index + 3]] = 0


def opcode_99():
    pass
    # print('Code has completed. output is: ', output)


def did_change(array, index, opcode):
    if ('0000' + str(array[index])) == opcode:
        return False
    else:
        return True


def get_params(array, modes, index):
    params = []
    modes = modes[::-1]
    for i in range(len(modes)):
        v = int(array[index + i + 1])
        if modes[i] == '0':
            params.append(array[v])
        elif modes[i] == '1':
            params.append(v)
    return params


class OpcodeComp:
    def __init__(self, array):
        self.memory = list(array)
        self.input = 0
        self.phase = 0
        self.output = 0
        self.index = 0
        self.finished = False
        self.isPhase = True

    def set_phase(self, val: int):
        self.phase = val

    def set_input(self, val: int):
        self.input = val

    def read_input(self):
        if self.isPhase:
            self.isPhase = False
            return self.phase
        else:
            return self.input

    def has_finished(self):
        return self.finished

    def set_output(self, val: int):
        self.output = val

    def get_output(self):
        return self.output

    def run_opcode(self):
        while not self.finished:
            # init fn, get method code from opcode str
            opcode = str(self.memory[self.index])
            opcode = '0000' + opcode
            fn = opcode[-2:]

            if fn == '01':
                opcode_1(self.memory, opcode[-5:-2], self.index)
                count = 4
            elif fn == '02':
                opcode_2(self.memory, opcode[-5:-2], self.index)
                count = 4
            elif fn == '03':
                input_val = self.read_input()
                opcode_3(self.memory, self.index, input_val)
                count = 2
            elif fn == '04':
                self.output = opcode_4(self.memory, self.index)
                # print('Output: ',self.output)
                self.index += 2
                break
            elif fn == '05':
                self.index = opcode_5(self.memory, opcode[-4:-2], self.index)
                count = 3
            elif fn == '06':
                self.index = opcode_6(self.memory, opcode[-4:-2], self.index)
                count = 3
            elif fn == '07':
                opcode_7(self.memory, opcode[-5:-2], self.index)
                count = 4
            elif fn == '08':
                opcode_8(self.memory, opcode[-5:-2], self.index)
                count = 4
            elif fn == '99':
                opcode_99()
                self.finished = True
                break
            else:
                print('Error')
                break

            # increment in case where instruction pointer has not changed
            if did_change(self.memory, self.index, opcode):
                continue
            else:
                self.index += count
                continue
        return 'Error'
