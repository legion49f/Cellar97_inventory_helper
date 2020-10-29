class Inventory(object):
    def __init__(self, db_filepath):
        self.db_filepath = db_filepath
        scanned_data = {}
        sorted_valid_items = []
        lookup_table = {}
        categories = [] 
        
    def split_into_chars(self, word:str):
        return [ char for char in word ]

    def parse_scanner_data(self, scanned_data:list):
        self.scanned_data = {}
        for line in scanned_data.splitlines():
            try:
                item = line.split()
                if len(item) == 3:
                    self.scanned_data[item[1]] = item
            except:
                continue
    
    def get_categories(self, valid_items:list):
        categories = set()
        for item in valid_items:
            categories.add(item[5])
        self.categories = list(categories)

    def get_valid_items(self, filename:str) -> list:
        sku, reg_price, name, stock, upc_code, category = 0, 7, 1, 11, 12 ,13
        valid_items = []
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.split('\t')
                try:
                    qty = int(line[11])
                    if line[12].isdigit():
                        if len( self.split_into_chars(line[12]) ) >= 5 :
                            valid_items.append( [ line[sku], line[reg_price], line[name], line[stock], line[upc_code], line[category] ])
                except:
                    continue
        return valid_items

    def sort_by_categories(self, valid_items:list):
        valid_items.sort(key=lambda x: x[5])
        self.sorted_valid_items = valid_items

    def get_lookup_table(self, valid_items:list) -> dict:
        self.lookup_table = {}
        for item in valid_items:
            self.lookup_table[ item[4] ] = item

    def import_database_file(self):
        valid_items = self.get_valid_items(self.db_filepath)
        self.sort_by_categories(valid_items)
        self.get_lookup_table(valid_items)