import time

with open('16/input.txt','r') as input_file:
    initial_state = list(map(int,list(input_file.read())))

# base_pattern = [0,1,0,-1]
length = len(initial_state)

pos_d = {}
neg_d = {}

def get_pos_indexes(i, l=length):

    if i < length/4:
        n,k = 0,0
        out = []
        while True:
            r = n*4*(i+1) + k + i
            if r > (l-1):
                break
            out.append(r)
            k += 1
            if k > i:
                k = 0
                n += 1
        return out
    else:
        return(list(range(i,(min(2*i +1, l)))))

    
        
def get_neg_indexes(i, l=length):

    if i < length/4:
        out = []
        n,k = 0,0
        while True:
                r = (i+1) * (4*n + 3) + k - 1
                if r > (l-1):
                    break
                out.append(r)
                k += 1
                if k > i:
                    k = 0
                    n += 1
        return out
    else: return []

for i in range(length):
    pos_d[i] = get_pos_indexes(i)
    neg_d[i] = get_neg_indexes(i)

def apply_pattern(state, i, l = length):
    lim = l/4
    if i < l/4:
        pos, neg = pos_d[i], neg_d[i]
        t = 0
        for p in pos:
            t += state[p]
        for n in neg:
            t -= state[n]
        return t
    else:
        return sum(state[i:2*i+1])

def get_dig(val):
    return val % 10

def perform_phase(state):
    l = [apply_pattern(state, i) for i in range(length)]
    return list(map(get_dig,l))

def iter_phase(state, count):
    i=0
    while i < count:
        state = perform_phase(state)
        i += 1
    return(state)

# Part 1
print(''.join(map(str,iter_phase(initial_state,100)[:8])))

# Part 2

offset = int(''.join(map(str,initial_state[0:7])))
# print(offset)

real_signal = []
COUNT_REPEAT_INPUT = 10000
for _ in range(COUNT_REPEAT_INPUT):
    real_signal += initial_state

signal = real_signal[offset:]
    
def perform_large_phase(offset_state):
    out = []
    last_num = 0
    for i in range(len(offset_state)):
        n = (last_num + offset_state[-(i+1)])%10
        out.append(n)
        last_num = n
    return out[::-1]

def iter_offset_phase(signal,iter_len):
    if len(signal) > (length * COUNT_REPEAT_INPUT )//2:
        print('Error: signal is too long, has not been offset correctly')
        return

    for _ in range(iter_len):
        signal = perform_large_phase(signal)

    return ''.join(map(str,signal))

st_time = time.time()
final_signal =iter_offset_phase(signal,100)
end_time = time.time()

print(final_signal[:8])
print("time to complete:", end_time-st_time)

