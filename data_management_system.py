import sqlite3

def split_into_chars(word:str):
    return [ char for char in word ]

def csv_to_hashmap_filtered(filename:str):
    sku, reg_price, name, stock, upc_code = 0, 7, 1, 11, 12
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
                                placeholder.append([ line[sku], line[reg_price], line[name], line[stock], line[upc_code] ] )
                                hashmap[ line[0] ] = placeholder
                            else:
                                # make product
                                hashmap[ line[0] ] = [ line[sku], line[reg_price], line[name], line[stock], line[upc_code] ]
            except:
                continue
    return hashmap

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

if __name__ == "__main__":
    hashmap = csv_to_hashmap_filtered("br-union.csv")
    add_csv_data_to_db(hashmap)

    
    print("done")