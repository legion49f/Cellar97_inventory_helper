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

def add_csv_data_to_db(csv_data):

    connection = sqlite3.connect("cellar97.db")
    cursor = connection.cursor()

    sql_command=""" CREATE TABLE employee ( staff_number INT NOT NULL, fname VARCHAR(20), lname VARCHAR(30), gender CHAR(1), 
        joining DATE, birth_date DATE, PRIMARY KEY (staff_number) ); """

    sql_command=""" USE TABLE employee; """
    sql_command=""" SELECT * FROM employee; """

    cursor.execute(sql_command)
    cursor.execute(sql_command)
    cursor.execute(sql_command)

if __name__ == "__main__":
    hashmap = csv_to_hashmap_filtered("br-union.csv")
    for key in hashmap:
        print(hashmap[key])
        pass
        
    # print(hashmap['74188'])
    print("done")