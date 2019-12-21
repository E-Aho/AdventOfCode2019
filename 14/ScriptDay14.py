import re
from collections import defaultdict
import time


def get_reaction_dict(raw):
    pattern = re.compile('\d+ \w+')

    reactions = {}
    for line in raw:
        reaction = [(name, int(v)) for v, name in [item.split(' ') for item in re.findall(pattern, line)]]
        name_out, vol_out = reaction[-1]
        reactions[name_out] = (vol_out, reaction[:-1])
    return reactions


def get_fuel(vol_fuel):
    # NB: Assumes all products come from a single reaction, and all reactions make only 1 product (tree like structure)
    ore_used = 0
    product_dict = {'FUEL': vol_fuel}
    reagent_dict = defaultdict(int)

    while len(product_dict) > 0:
        prod, prod_vol = list(product_dict.items())[0]
        del product_dict[prod]

        times_performed = -(-prod_vol // reaction_dict[prod][0])  # double negative here to get ceil division
        reagent_dict[prod] += (reaction_dict[prod][0] * times_performed) - prod_vol

        for reagent, reagent_vol in reaction_dict[prod][1]:
            vol_needed = (reagent_vol * times_performed)
            if reagent == 'ORE':
                ore_used += vol_needed
            else:
                remaining_vol = reagent_dict[reagent]
                vol_to_make = vol_needed - remaining_vol
                if vol_to_make > 0:
                    reagent_dict[reagent] = 0
                    product_dict[reagent] = product_dict.get(reagent, 0) + vol_to_make
                else:
                    reagent_dict[reagent] -= vol_needed

    return ore_used


def binary_search_fuel(ore_vol):
    min_fuel, max_fuel = 1, 100000000
    midpoint = None
    while max_fuel - min_fuel > .01:
        midpoint = (min_fuel + max_fuel) / 2
        ore_needed = get_fuel(int(midpoint))
        if ore_needed > ore_vol:
            max_fuel = midpoint
        else:
            min_fuel = midpoint
    return int(midpoint)


if __name__ == '__main__':

    with open('14/input.txt', 'r') as file:
        reactions_raw = file.read().splitlines()

    reaction_dict = get_reaction_dict(reactions_raw)

    start_time1 = time.time()
    print('\nPart 1:')
    print('Ore needed to get 1 unit of fuel: ', get_fuel(1))
    end_time1 = time.time()

    start_time2 = time.time()
    print('\nPart 2:')
    ore_cap = 1000000000000
    print('Volume of fuel from 1 trillion units of ore:', binary_search_fuel(ore_cap))
    end_time2 = time.time()
    print('\nTimings:\nPart 1: %.4fs\nPart 2: %.4fs' % (end_time1-start_time1, end_time2-start_time2))
