# NB: probably could clean this up using classes for instructions but this works and is still pretty clear
# Only problem is maybe that param[2] isn't as clear with what it is doing as it could be but oh well
import time


def get_initial_state():  # could do with deep copy instead of fetching each time
    with open('05/input.txt', 'r') as input_file:
        return list(map(int, input_file.read().split(',')))


# Define functions to be called
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


def opcode_1(array, modes, index):
    params = get_params(array, modes, index)
    array[(array[index + 3])] = params[1] + params[0]


def opcode_2(array, modes, index):
    params = get_params(array, modes, index)
    array[(array[index + 3])] = params[1] * params[0]


def opcode_3(array, modes, index):
    address = array[index + 1]
    val = int(input("Enter a value for Opcode 3 at index %i \n" % index))
    array[address] = val


def opcode_4(array, modes, index):
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
    print('Code has completed.')


def did_change(array, index, opcode):
    if ('0000' + str(array[index])) == opcode:
        return False
    else:
        return True


# initialize before running through loop


# run through intcode
# only increment index by count( of values accessed )IF the instruction pointer didn't change

def run_opcode(array):
    output = None
    index = 0
    while True:
        # init fn, get method code from opcode str
        opcode = str(array[index])
        opcode = '0000' + opcode
        fn = opcode[-2:]
        print('fn: ', fn)

        # perform needed opcode fn
        if fn == '01':
            opcode_1(array, opcode[-5:-2], index)
            count = 4
        elif fn == '02':
            opcode_2(array, opcode[-5:-2], index)
            count = 4
        elif fn == '03':
            opcode_3(array, '', index)
            count = 2
        elif fn == '04':
            output = opcode_4(array, '', index)
            print('Output: ', output)
            count = 2
        elif fn == '05':
            index = opcode_5(array, opcode[-4:-2], index)
            count = 3
        elif fn == '06':
            index = opcode_6(array, opcode[-4:-2], index)
            count = 3
        elif fn == '07':
            opcode_7(array, opcode[-5:-2], index)
            count = 4
        elif fn == '08':
            opcode_8(array, opcode[-5:-2], index)
            count = 4
        elif fn == '99':
            opcode_99()
            break
        else:
            print('Error')
            break

        # increment in case where instruction pointer has not changed
        if did_change(array, index, opcode):
            continue
        else:
            index += count
            continue
    return output


if __name__ == '__main__':
    start_time = time.time()
    initial_array = get_initial_state()
    print(run_opcode(initial_array))
    end_time = time.time()
    print('\nCompleted in %.4fs' % (end_time - start_time))
