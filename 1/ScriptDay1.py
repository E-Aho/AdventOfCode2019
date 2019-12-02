with open('1/input.txt', 'r') as input_file:
    modules = input_file.read().splitlines()

fuel_sum = 0

def get_fuel(mass):
    return ((mass // 3) - 2)

for module in modules:
    mass = int(module)
    fuel_sum += get_fuel(mass)

print('\nFuel sum for first task = ', fuel_sum) #Answer to part 1

def get_fuel_recursion(mass):
    fuel_tot = 0
    fuel_mass = get_fuel(mass)
    if fuel_mass > 0:
        fuel_tot += fuel_mass + get_fuel_recursion(fuel_mass)
    return fuel_tot

fuel_rec_sum = 0
for module in modules:
    mass = int(module)
    fuel_rec_sum += get_fuel_recursion(mass)
    
print('Recursive total fuel for second task = ', fuel_rec_sum, '\n') #Answer to part 2