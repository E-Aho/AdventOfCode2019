import time


def get_fuel(m):
    return (m // 3) - 2


def part_1(inp):
    fuel_sum = 0

    for module_mass in inp:
        m = int(module_mass)
        fuel_sum += get_fuel(m)

    return fuel_sum


def get_fuel_recursive(m):
    fuel_tot = 0
    fuel_mass = get_fuel(m)
    if fuel_mass > 0:
        fuel_tot += fuel_mass + get_fuel_recursive(fuel_mass)
    return fuel_tot


def part_2(inp):
    fuel_rec_sum = 0
    for module in inp:
        mass = int(module)
        fuel_rec_sum += get_fuel_recursive(mass)
    return fuel_rec_sum


if __name__ == "__main__":
    with open('1/input.txt', 'r') as input_file:
        input_list = input_file.read().splitlines()

    print('\nRunning Day 1 Script\n')
    start_time = time.time()
    print('\nPart 1: \nFuel sum for first task = ', part_1(input_list))
    print('\nPart 2: \nRecursive total fuel for second task = ', part_2(input_list), '\n')
    end_time = time.time()

    print('\nTotal time to complete: %.6fs' % (end_time - start_time))
