import urllib.request
import json
import subprocess
from os import chdir
import csv
import time


def split_into_chars(word:str):
    return [ char for char in word ]

def trigger_export(link:str):
    req = urllib.request.Request(link)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
        print(the_page)

def process_export(link:str):
    condition = True
    while condition:
        json_obj = json.load(urllib.request.urlopen(link))
        print(json_obj['message'])
        condition = 'Export' and 'complete' not in json_obj['message']

def run_wget(link:str):
    print('Running Wget')
    req = urllib.request.Request(link)
    with urllib.request.urlopen(req) as response:
        content = response.read()
    with open('/home/cellar97/parsed-products/woo_db_export.csv', 'w') as f:
        f.write( content.decode("utf-8") )
    print('Wget Done')

def to_hashmap_with_filtered_columns(filename:str):
    sku, reg_price, name, stock = 0, 7, 1, 11
    hashmap = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            placeholder = []
            line = line.split('\t')
            try:
                if line[12].isdigit() and line[11].isdigit():
                    if len( split_into_chars(line[12]) ) > 5 :
                        # if int(line[11]) > 0:
                        if True:
                            if line[0] in hashmap:
                                for row in hashmap[ line[1] ]:
                                    placeholder.append( row )
                                placeholder.append([ line[sku], line[reg_price], line[name], line[stock] ] )
                                hashmap[ line[0] ] = placeholder
                            else:
                                # make product
                                hashmap[ line[0] ] = [ line[sku], line[reg_price], line[name], line[stock] ]
            except:
                continue
    return hashmap

def generate_import_csv(hashmap:dict, filename:str, savefile:str):
    generated_data = []
    with open(filename, 'r', encoding='utf-8') as f:
        table_header = f.readline()
        readCSV = csv.reader(f, delimiter=',')
        for row in readCSV:
            sku, reg_price, stock = row[4], row[2], row[6]
            try:
                if sku != hashmap[sku][0] or reg_price != hashmap[sku][1] or stock != hashmap[sku][3]:
                    row[4], row[2], row[6] = hashmap[sku][0], hashmap[sku][1], hashmap[sku][3]
                    generated_data.append(row)
            except KeyError:
                # print('Key not found', sku)
                pass
    GENERATED_FILE_NAME = savefile
    if generated_data is not None:
        with open(GENERATED_FILE_NAME, 'w', newline='\r', encoding='utf-8') as file:
            file.write(table_header)
            for row in generated_data:
                row[2] = "\"" + row[2] + "\""
                row[3] = "\"" + row[3] + "\""
                row[5] = "\"" + row[5] + "\""
                row[7] = "\"" + row[7] + "\""
                row[8] = "\"" + row[8] + "\""
                row[9] = "\"" + row[9] + "\""
                for i in range(0, 10):
                    if i == 9:
                        file.write(row[i] + '\r')
                    else:
                        file.write(row[i] + ',')

def trigger_import(link:str):
    req = urllib.request.Request(link)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
        print(the_page)

def process_import(link:str):
    condition = True
    while condition:
        json_obj = json.load(urllib.request.urlopen(link))
        print(json_obj['message'])
        condition = 'Import' and 'complete' not in json_obj['message']

if __name__ == "__main__":
    # chdir('/home/cellar97/')
    # trigger_export(r'https://cellar97.com/wp-load.php?export_key=xpdOD7tHZ7BW&export_id=12&action=trigger')
    # time.sleep(5)
    # process_export(r'https://cellar97.com/wp-load.php?export_key=xpdOD7tHZ7BW&export_id=12&action=processing')

    # run_wget("https://cellar97.com/wp-load.php?security_token=7aa82581e89d9cfb&export_id=12&action=get_data")

    testing = True
    if not testing:
        br_union_hashmap = to_hashmap_with_filtered_columns('/home/cellar97/productlist/br-union.csv') #tested
        generate_import_csv(br_union_hashmap, '/home/cellar97/parsed-products/woo_db_export.csv', '/home/cellar97/public_html/wp-content/uploads/wpallimport/files/import_me.csv')
    else:
        br_union_hashmap = to_hashmap_with_filtered_columns('br-union.csv') #tested
        # print( br_union_hashmap.keys() )
        print( br_union_hashmap['00045'] )
        generate_import_csv(br_union_hashmap, 'woo_db_export.csv', 'import_me.csv')

    # trigger_import(r'https://cellar97.com/wp-load.php?import_key=j5zxUCWd&import_id=8&action=trigger')
    # time.sleep(5)
    # process_import(r'https://cellar97.com/wp-load.php?import_key=j5zxUCWd&import_id=8&action=processing')