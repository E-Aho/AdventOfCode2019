finish_iter = False

def get_initial_state(): #could do with deep copy instead of fetching each time
    with open('5/input.txt', 'r') as input_file:
        return(list(map(int, input_file.read().split(','))))

#Define functions to be called 

def get_params(array, modes, index):
    params = []
    modes = modes[::-1]
    for i in range(len(modes)):
        v = int(array[index+i+1])
        if modes[i] == '0':
            params.append(array[v])
        elif modes[i] == '1':
            params.append(v)
    return params
   
def opcode_1(array, modes, index):
    params = get_params(array,modes,index)
    array[(array[index+3])]= params[1] + params[0]

def opcode_2(array, modes, index):
    params = get_params(array,modes,index)
    array[(array[index+3])] = params[1] * params[0]

def opcode_3(array, modes, index):
    address = array[index+1]
    val = int(input("Enter a value for opcode 3\n"))
    array[address] = val

def opcode_4(array, modes, index):
    address = int(array[index+1])
    return(int(array[address]))

def opcode_5(array, modes, index):
    params = get_params(array,modes,index)
    if params[0] != 0:
        return(params[1])
    else: 
        return(index)

def opcode_6(array, modes, index):
    params = get_params(array, modes,index)
    if params[0] == 0:
        return(params[1])
    else:
        return(index)

def opcode_7(array, modes, index):
    params = get_params(array, modes, index)
    if params[0] < params[1]:
        array[array[index+3]] = 1
    else:
        array[array[index+3]] = 0

def opcode_8(array, modes, index):
    params = get_params(array, modes, index)
    if params[0] == params[1]:
        array[array[index+3]] = 1
    else:
        array[array[index+3]] = 0

def opcode_99():
    print('Code has completed.')

def did_change(array, index, opcode):
    if ('0000' + str(array[index])) == opcode:
        return False
    else: 
        return True

#initialize before running through loop
index = 0
array = get_initial_state()
finish_iter = False


#run through intcode
#only increment index by count( of values accessed )IF the instruction pointer didn't change
while finish_iter == False: 
    #init fn, get method code from opcode str
    count = 0
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
        print('Output: ',opcode_4(array, '', index))
        count = 2
    elif fn == '05':
        index = opcode_5(array, opcode[-4:-2], index)
        count = 3
    elif fn == '06':
        index = opcode_6(array, opcode[-4:-2], index)
        count = 3
    elif fn == '07':
        opcode_7(array, opcode[-5:-2], index)
        count =  4
    elif fn == '08':
        opcode_8(array, opcode[-5:-2], index)
        count = 4
    elif fn == '99':
        opcode_99()
        finish_iter = True
        break
    else:
        print('Error')
        break

    #increment in case where instruction pointer has not changed
    if did_change(array, index, opcode): 
        continue
    else:
        index += count
        continue
 