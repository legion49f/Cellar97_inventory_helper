import random
from random import randint

def split_into_chars( word:str):
    return [ char for char in word ]

def get_valid_items( filename:str) -> list:
    sku, reg_price, name, stock, upc_code, category = 0, 7, 1, 11, 12 ,13
    valid_items = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.split('\t')
            try:
                qty = int(line[11])
                if line[12].isdigit():
                    if len( split_into_chars(line[12]) ) >= 5 :
                        valid_items.append( [ line[sku], line[reg_price], line[name], line[stock], line[upc_code], line[category] ])
            except:
                continue
    return valid_items

def get_categories(valid_items:list):
    categories = set()
    for item in valid_items:
        categories.add(item[5])
    return list(categories)

def sort_by_categories(valid_items:list):
    valid_items.sort(key=lambda x: x[5])
    return valid_items

def get_lookup_table(valid_items:list) -> dict:
    lookup_table = {}
    for item in valid_items:
        lookup_table[ item[5] ] = item
    return lookup_table

def generate_testing_data(valid_items:list, items_to_gen:int):
    randoms = random.sample(range(0, len(valid_items)), items_to_gen)
    with open('testing_data.txt', 'w', encoding='utf-8') as f:
        for item in randoms:
            f.write('BRUNION\t' + valid_items[item][4] +'\t' + str(randint(1,50)) +'\n')

if __name__ == '__main__':
    valid_items = get_valid_items('./csv files/br-union.csv')
    sorted_items = sort_by_categories(valid_items)
    lookup_table = get_lookup_table(valid_items)
    generate_testing_data(valid_items, 500)
    print('Done')