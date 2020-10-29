import json
import csv
from os import chdir
from typing import NoReturn

def split_into_chars(word:str):
    return [ char for char in word ]

def format_br_union(filename:str, formatted:str):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
        text = text.replace('\t', ',')
    with open(formatted, 'w', encoding='utf-8') as f:
        f.write(text)

def item_count():
    hashmap = {}
    with open('br-union.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.split('\t')
            line = list( filter(None, line) )
            if line[1] in hashmap:
                # if product exist append
                hashmap.setdefault( line[1], [] ).append( line[:-1] )
            else:
                # make product    
                hashmap[ line[1] ] = line[:-1]

    with open('items_list.txt', 'w', encoding='utf-8') as f:
    	count = 1
    	for item in hashmap:
    		f.write(str(count)+' '+item + '\n')
    		count+=1

    return hashmap

def to_hashmap(filename:str):
    hashmap = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            placeholder = []
            line = line.split('\t')
            try:
                if line[12].isdigit() and line[11].isdigit():
                    if len( split_into_chars(line[12]) ) > 5 :
                        if int(line[11]) > 0:
                            if line[1] in hashmap:
                                for row in hashmap[ line[1] ]:
                                    placeholder.append(row)
                                placeholder.append(line[:-1])
                                hashmap[ line[1] ] = placeholder
                            else:
                                # make product
                                placeholder.append( line[:-1] ) 
                                hashmap[ line[1] ] = placeholder
            except:
                continue
    return hashmap

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

def pop_by_name(product_name:str):
    data = []
    with open('br-union.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.split('\t')
            # print(line)
            # line = list( filter(None, line) )
            if product_name in line:
                data.append(line)

    with open('item.txt','w', encoding='utf-8') as f:
        for line in data:
            f.write( str(line[:-1]) + '\n' )

    with open('item.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for line in data:
            writer.writerow(line)

def unique_items_to_csv():
    items_list = []
    with open('br-union.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.split('\t')
            
            if any(line[1] in sublist for sublist in items_list):
                continue

            elif line[12].isdigit() and line[11].isdigit():
                if len( split_into_chars(line[12]) ) > 5 :
                    if int(line[11]) > 0:
                        items_list.append(line)

    with open('unique_items_list.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in items_list:
            writer.writerow(row)

def items_to_csv():
    items_list = []
    with open('br-union.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.split('\t')

            if line[12].isdigit() and line[11].isdigit():
                if len( split_into_chars(line[12]) ) > 5 :
                    if int(line[11]) > 0:
                        items_list.append(line)

    with open('items_list.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in items_list:
            writer.writerow(row)

def items_with_zero_stock_to_csv():
    items_list = []
    with open('br-union.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.split('\t')

            if line[12].isdigit() and line[11].isdigit():
                if len( split_into_chars(line[12]) ) > 5 :
                    if int(line[11]) == 0:
                        items_list.append(line)

    with open('items_with_zero_stock_list.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in items_list:
            writer.writerow(row)

def unique_items_with_zero_stock_to_csv():
    items_list = []
    with open('br-union.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.split('\t')

            if line[12].isdigit() and line[11].isdigit():
                if len( split_into_chars(line[12]) ) > 5 :
                    if int(line[11]) == 0:            
                        if any(line[1] in sublist for sublist in items_list):
                            continue
                        else:
                            items_list.append(line)

    with open('unique_items_with_zero_stock_list.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in items_list:
            writer.writerow(row)

def write_to_csv(hashmap:dict, filename:str):
    print('Starting:')
    # 44 is the number of columns
    first_row = ['ID','Type','SKU','Name','Published','Is featured?','Visibility in catalog','Short description',\
        'Description','Date sale price starts','Date sale price ends','Tax status','Tax class','In stock?','Stock',\
        'Low stock amount','Backorders allowed?','Sold individually?','Weight (kg)','Length (cm)','Width (cm)',\
        'Height (cm)','Allow customer reviews?','Purchase note','Sale price','Regular price','Categories','Tags',\
        'Shipping class','Images','Download limit','Download expiry days','Parent','Grouped products','Upsells',\
        'Cross-sells','External URL','Button text','Position','Attribute 1 name','Attribute 1 value(s)',\
        'Attribute 1 visible','Attribute 1 global','Attribute 1 default']

    ID = 0 #increment every time you finish an item and sub items
    Type = ''
    SKU = ''
    Name = ''
    Published = '1'
    Is_featured = '0'
    Visibility_in_catalog = 'visible'
    Short_description = ''
    Description = ''
    Date_sale_price_starts = ''
    Date_sale_price_ends = ''
    Tax_status = 'taxable'
    Tax_class = '' # says parent when its a variation
    In_stock = '1'
    Stock = '' # get from hashmap
    Low_stock_amount = ''
    Backorders_allowed = '0'
    Sold_individually = '0'
    Weight_kg = ''
    Length_cm =''
    Width_cm = ''
    Height_cm = ''
    Allow_customer_reviews = ''
    Purchase_note = ''
    Sale_price = ''
    Regular_price = ''
    Categories = ''
    Tags = ''
    Shipping_class = ''
    Images = ''
    Download_limit = ''
    Download_expiry_days = ''
    Parent = ''
    Grouped_products = ''
    Upsells = ''
    Cross_sells = ''
    External_URL = ''
    Button_text = ''
    Position = 0
    Attribute_1_name = 'Size'
    Attribute_1_values = ''
    Attribute_1_visible = '1'
    Attribute_1_global = '1'
    Attribute_1_default = '' # the first one

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(first_row)
        for items in hashmap.values(): #some items are a list of lists and some are just individual items needs to make a check here to work on them differently.
            # if any(isinstance(el, list) for el in items ): #if its a list of lists is a variable item
            if len(items) > 1:
                # logic for variable
                # note add short description
                row = items[0]
                # print('Variation Item:', row)
                ID+=1
                Allow_customer_reviews = '1'
                Type = 'variable'
                SKU = ''
                Name = row[1]
                Tax_class = ''
                Stock = ''
                Short_description = row[23]
                Parent = ''
                Position = 0
                Regular_price = ''
                Attribute_1_values = '' #row[4]
                for item in items:
                    Attribute_1_values += item[4] +', '
                Attribute_1_values = Attribute_1_values[:-2]
                Attribute_1_visible = 1
                Attribute_1_default = row[4]
                Categories = row[13] +' > ' + row[14] +' > ' + row[15]

                col_data_for_variation = [ID, Type, SKU, Name, Published, Is_featured, Visibility_in_catalog, Short_description, Description,\
                    Date_sale_price_starts, Date_sale_price_ends, Tax_status, Tax_class, In_stock, Stock, Low_stock_amount, Backorders_allowed,\
                    Sold_individually, Weight_kg, Length_cm, Width_cm, Height_cm, Allow_customer_reviews, Purchase_note, Sale_price, Regular_price,\
                    Categories, Tags, Shipping_class, Images, Download_limit, Download_expiry_days, Parent, Grouped_products, Upsells, Cross_sells,\
                    External_URL, Button_text, Position, Attribute_1_name, Attribute_1_values, Attribute_1_visible, Attribute_1_global, Attribute_1_default ]
                writer.writerow(col_data_for_variation)
                
                Parent_ID = ID
                for row in items:
                    # pass
                    # print('Variable Item:', row)
                    Parent = 'id:' + str(Parent_ID)
                    ID+=1
                    Position+=1
                    Allow_customer_reviews = '0'
                    Type = 'variation'
                    SKU = row[0]
                    Name = row[1] + '-' + row[4]
                    Tax_class = ''
                    Stock = row[11]
                    Regular_price = row[7]
                    Attribute_1_values = row[4]
                    Short_description = ''
                    Categories = ''

                    col_data_for_variation = [ID, Type, SKU, Name, Published, Is_featured, Visibility_in_catalog, Short_description, Description,\
                        Date_sale_price_starts, Date_sale_price_ends, Tax_status, Tax_class, In_stock, Stock, Low_stock_amount, Backorders_allowed,\
                        Sold_individually, Weight_kg, Length_cm, Width_cm, Height_cm, Allow_customer_reviews, Purchase_note, Sale_price, Regular_price,\
                        Categories, Tags, Shipping_class, Images, Download_limit, Download_expiry_days, Parent, Grouped_products, Upsells, Cross_sells,\
                        External_URL, Button_text, Position, Attribute_1_name, Attribute_1_values, Attribute_1_visible, Attribute_1_global, Attribute_1_default ]
                    writer.writerow(col_data_for_variation)
            else:
                # print('Simple Item:', items)
                # pass
                row = items[0]
                ID+=1
                Allow_customer_reviews = '1'
                Type = 'simple'
                SKU = row[0]
                Name = row[1]
                Tax_class = ''
                Stock = row[11]
                Short_description = row[23]
                Regular_price = row[7]
                Attribute_1_values = row[4]
                Parent = ''
                Position = 0
                Categories = row[13] +' > ' + row[14] +' > ' + row[15]

                col_data_for_variation = [ID, Type, SKU, Name, Published, Is_featured, Visibility_in_catalog, Short_description, Description,\
                    Date_sale_price_starts, Date_sale_price_ends, Tax_status, Tax_class, In_stock, Stock, Low_stock_amount, Backorders_allowed,\
                    Sold_individually, Weight_kg, Length_cm, Width_cm, Height_cm, Allow_customer_reviews, Purchase_note, Sale_price, Regular_price,\
                    Categories, Tags, Shipping_class, Images, Download_limit, Download_expiry_days, Parent, Grouped_products, Upsells, Cross_sells,\
                    External_URL, Button_text, Position, Attribute_1_name, Attribute_1_values, Attribute_1_visible, Attribute_1_global, Attribute_1_default ]
                writer.writerow(col_data_for_variation)
    print('Finished')

def generate_import_csv(hashmap:dict, filename:str):
    generated_data = []
    with open(filename, 'r') as f:
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
    GENERATED_FILE_NAME = 'import_me.csv'           
    if generated_data is not None:
        with open(GENERATED_FILE_NAME, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            file.write(table_header)
            for row in generated_data:
                writer.writerow(row)

def generate_sorted_csv(infile:str, outfile:str) -> NoReturn:
    with open(infile, 'r', encoding='utf-8') as f:
        data = []
        for line in f.readlines():
            placeholder = []
            line = line.split('\t')
            for item in line[:-1]:
                placeholder.append(item)
            data.append(placeholder)
            
    data.sort(key=lambda x: x[14])
    with open(outfile, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        for line in data:
            writer.writerow(line)

def get_unique_categories(filename:str):
    data = set()
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.split('\t')
            data.add(line[13])
    data = list(data)
    data.sort()

def add_csv_data_to_db(csv_data:dict):
    connection = sqlite3.connect("cellar97.db")
    with connection:
        cursor = connection.cursor()

        cursor.execute(""" DROP TABLE products; """)

        sql_command="""CREATE TABLE products ( sku INT NOT NULL, price FLOAT, item_name VARCHAR(255), stock_quantity INT, 
            upc_code VARCHAR(15), PRIMARY KEY (sku) );"""
        cursor.execute(sql_command)

        for key in csv_data:
            item_name = "".join(e for e in csv_data[key][2] if e.isalnum() or e == " ")
            command = F"""INSERT INTO products(sku, price, item_name, stock_quantity, upc_code) VALUES
                ({csv_data[key][0]}, {csv_data[key][1]}, "{item_name}",
                {csv_data[key][3]}, {csv_data[key][4]} );"""
            print(command)
            cursor.execute(command)

        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

def main():
    # chdir('/home/cellar97/Public_HTML/')
    # br_union_hashmap = to_hashmap_with_filtered_columns('br-union.csv') #tested
    # print(br_union_hashmap.keys() )
    # print(br_union_hashmap['00418'] )
    # print(br_union_hashmap['00419'] )
    # print(br_union_hashmap['00420'] )
    # print(br_union_hashmap['00423'] )
    # print(br_union_hashmap['02135'] )
    # print(br_union_hashmap['03979'] )
    # print(br_union_hashmap['06569'] )
    # generate_import_csv(br_union_hashmap, 'woo_db_export.csv')
    # generate_sorted_csv('br-union.csv', 'sorted_csv.csv')
    get_unique_categories('br-union.csv')
    
if __name__ == "__main__":
    main()