import time


# Part 1
def check_fit(passcode):
    passcode = str(passcode)
    double = 0
    for i in range(len(passcode) - 1):
        if passcode[i] == passcode[i + 1]:
            double += 1
        elif int(passcode[i]) > int(passcode[i + 1]):
            return False
    if double == 0:
        return False
    elif double > 0:
        return True
    else:
        print('error')
        return False


# Part 2
def second_check_fit(passcode):  # works in O(n), only one pass
    double = 0
    counter = 0
    passcode = str(passcode)
    for i in range(len(passcode) - 1):
        if passcode[i] > passcode[i + 1]:
            return False
        elif passcode[i] == passcode[i + 1]:
            counter += 1
        elif passcode[i] < passcode[i + 1]:
            if counter == 1:
                counter = 0
                double += 1
            else:
                counter = 0
    if counter == 1:  # needed to catch case where double occurs in last two numbers
        double += 1
    if double == 0:
        return False
    if double > 0:
        return True
    else:
        print('error in second check')
        return False


if __name__ == "__main__":

    print('\nRunning Day 4 Script\n')
    min_input = 372037
    max_input = 905157
    start = time.time()

    count_fit = 0
    for code in range(min_input, max_input):
        if check_fit(code):
            count_fit += 1

    print('\nPart 1: \nThe solution to the first part is: ', count_fit)

    count_second_fit = 0
    for code in range(min_input, max_input):
        if second_check_fit(code):
            count_second_fit += 1
    end = time.time()

    print("\nPart 2: \nThe solution to the second part is: ", count_second_fit)
    print('\nTime to complete: %.4fs' % (end - start))
