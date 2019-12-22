import time


def get_pos_indexes(i, length):
    if i < length / 4:
        n, k = 0, 0
        out = []
        while True:
            r = n * 4 * (i + 1) + k + i
            if r > (length - 1):
                break
            out.append(r)
            k += 1
            if k > i:
                k = 0
                n += 1
        return out
    else:
        return list(range(i, (min(2 * i + 1, length))))


def get_neg_indexes(i, length):
    if i < length / 4:
        out = []
        n, k = 0, 0
        while True:
            r = (i + 1) * (4 * n + 3) + k - 1
            if r > (length - 1):
                break
            out.append(r)
            k += 1
            if k > i:
                k = 0
                n += 1
        return out
    else:
        return []


def get_indexes(length):
    p, n = {}, {}
    for i in range(length):
        p[i] = get_pos_indexes(i, length)
        n[i] = get_neg_indexes(i, length)
    return p, n


def apply_pattern(state, i):

    if i < len(state) / 4:
        pos, neg = pos_d[i], neg_d[i]
        t = 0
        for p in pos:
            t += state[p]
        for n in neg:
            t -= state[n]
        return t
    else:
        return sum(state[i:2 * i + 1])


def get_dig(val):
    return val % 10


def perform_phase(state):
    raw_arr = [apply_pattern(state, i) for i in range(signal_length)]
    return list(map(get_dig, raw_arr))


def iter_phase(state, count):
    i = 0
    while i < count:
        state = perform_phase(state)
        i += 1
    return state


# Part 1
# print(''.join(map(str, iter_phase(initial_state, 100)[:8])))

# Part 2


def perform_large_phase(offset_state):
    out = []
    last_num = 0
    for i in range(len(offset_state)):
        n = (last_num + offset_state[-(i + 1)]) % 10
        out.append(n)
        last_num = n
    return out[::-1]


def iter_offset_phase(signal, iter_len):
    if len(signal) > (signal_length * COUNT_REPEAT_INPUT) // 2:
        print('Error: signal is too long, has not been offset correctly')
        return

    for _ in range(iter_len):
        signal = perform_large_phase(signal)

    return ''.join(map(str, signal))


# print(final_signal[:8])
# print("time to complete:", end_time - start_time)

if __name__ == '__main__':
    start_time_1 = time.time()

    with open('16/input.txt', 'r') as input_file:
        initial_state = list(map(int, list(input_file.read())))

    # base_pattern = [0,1,0,-1]
    signal_length = len(initial_state)
    pos_d, neg_d = get_indexes(signal_length)
    signal_code_1 = ''.join(map(str, iter_phase(initial_state, 100)))[:8]
    print("Part 1:\nCode:", signal_code_1)
    end_time_1 = time.time()

    # Part 2
    print("\nRunning Part 2...")
    start_time_2 = time.time()
    offset = int(''.join(map(str, initial_state[0:7])))
    real_signal = []
    COUNT_REPEAT_INPUT = 10000
    for _ in range(COUNT_REPEAT_INPUT):
        real_signal += initial_state
    offset_signal = real_signal[offset:]
    final_signal = iter_offset_phase(offset_signal, 100)
    print("Part 2:\nCode: ", final_signal[:8])
    end_time_2 = time.time()
    print('Timings: Part 1: %.4fs    Part 2: %.4fs' % (end_time_1 - start_time_1, end_time_2 - start_time_2))

