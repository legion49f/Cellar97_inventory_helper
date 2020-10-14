from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import wget

import Levenshtein
import time

def split_into_chars(word:str):
    return [ char for char in word ]

def get_items(filename):
    items_list = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.split('\t')

            if line[12].isdigit() and line[11].isdigit():
                if len( split_into_chars(line[12]) ) > 5 :
                    if int(line[11]) > 0:
                        items_list.append(line[1])
    return list(dict.fromkeys(items_list))

def get_items_with_substr(filename, subwords):
    items_list = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.split('\t')

            if any(subword in line[1] for subword in subwords ):
                for item in subwords:
                    line[1] = line[1].replace(item, '')
            else:
                continue

            if line[12].isdigit() and line[11].isdigit():
                if len( split_into_chars(line[12]) ) > 5 :
                    if int(line[11]) > 0:
                        items_list.append(line[1])
    return list(dict.fromkeys(items_list))

def get_closest_match(phrase, class_items):

    # test_list = ['BACARDÍ Limón Flavored White Rum', 'BACARDÍ Lime Flavored White Rum', 'BACARDĺ Ready to Drink Límon & Lemonade', \
    #     'BACARDĺ Ready to Drink Lime & Soda', 'Devils Backbone Vodka Soda Lime', 'Bacardi Major Lazer Limited Edition Rum', \
    #     'BACARDÍ Gran Reserva Limitada', 'Backyard Soda Co Ginger Lime']
    try:
        test_list = []

        for class_item in class_items:
            line = class_item.text
            line = line.replace('\n','\t')
            line = line.split('\t')[0]
            test_list.append(line)

        phrase = phrase.lower()
        tally = 100
        result = ''
        
        for item in test_list:
            test = item.lower()
            dist = Levenshtein.distance(phrase, test[:len(phrase)])
            if dist < tally:
                tally = dist
                result = item
    except:
        pass
    try:
        return test_list.index(result)
    except:
        return 0

def scrape_site(site, items_list):
    PATH = r'C:/Users/Legion49F/AppData/Roaming/Python/chromedriver.exe'
    # PATH = r'C:/Program Files (x86)/Chromedriver/84/chromedriver.exe'

    driver = webdriver.Chrome(PATH)
    

    for item in items_list:

        driver.get(site)
        search = driver.find_element_by_id('SearchField')
        search.send_keys(item)
        search.send_keys(Keys.RETURN)

        element = ''
        li_class_items = ''

        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "CatalogGrid__CatalogList___2sZUK"))
            )
            li_class_items = element.find_elements_by_class_name('CatalogItemCard__Wrapper___3ED7z')

            closest_match_index = get_closest_match(item, li_class_items)
            print('best fit index:', closest_match_index)

            link = li_class_items[closest_match_index]
            link.click()

        except:
            print('could not find item in way number 1:', item)

            try:
                element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "CatalogItemCard__Content___1Imos CatalogItemCard__CatalogContent___TXuml CatalogItemCard__CardBottomMargin___1hE9Q"))
                )
                li_class_items = element.find_elements_by_class_name('CatalogItemCard__Wrapper___3ED7z')

                closest_match_index = get_closest_match(item, li_class_items)
                print('best fit index:', closest_match_index)

                link = li_class_items[closest_match_index]
                link.click()

            except:
                print('could not find item way number 2:', item)

                try:
                    element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "CatalogItemCard__Content___1Imos CatalogItemCard__CatalogContent___TXuml CatalogItemCard__CardBottomMargin___1hE9Q"))
                    )
                    li_class_items = element.find_elements_by_class_name('CatalogItemCard__Wrapper___3ED7z')

                    closest_match_index = get_closest_match(item, li_class_items)
                    print('best fit index:', closest_match_index)

                    link = li_class_items
                    link.click()
                except:
                    print('could not find item way number 3:', item)
                    continue        

        
        try:
            element = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ProductMetaInformation__PackagingImageContainer___3STHU"))
            )
            div_item = driver.find_element_by_class_name('ProductMetaInformation__NoAddressImage___2ZBhg')
            image_url = div_item.get_attribute('src')
            print('image src:', image_url)

        except:
            print('cannot find image src for item:' , item)
            continue
        
        if image_url is not None:
            try:
                wget.download(image_url, out='./images/'+item + '.jpeg')

                element = driver.find_element_by_class_name('DrizlyStyles__Body___2uneq')
                product_description = element.text
                
                elements = driver.find_elements_by_class_name('PDPAttributesAndReviews__row__value___1EoK-')

                additional_info = []
                for element in elements:
                    add = element.text
                    additional_info.append(add)
                
                elements2 = driver.find_elements_by_class_name('PDPAttributesAndReviews__row__label___3DksY')

                additional_info2 = []
                for element2 in elements2:
                    add = element2.text
                    additional_info2.append(add)

                if product_description is not None:
                    with open('./images/'+item+'.txt', 'w') as f:
                        for i in range(len(additional_info)):
                            f.write(additional_info2[i]+': '+ additional_info[i] + '\n')
                        f.write('PRODUCT DESCRIPTION:'+ '\n' + product_description)

            except:
                print('failed to download image for item:', item)
                continue

    driver.close()

def main():
    # items = get_items('br-union.txt')
    subwords = ['NRS', '12 PAK', 'LOOSE', 'PK', '12', 'PAK']

    items2 = get_items_with_substr('br-union.txt', subwords)
    print('items with: PAK', items2)

    # result = get_closest_match('item', items)
    # scrape_site('https://drizly.com', items2)


if __name__ == '__main__':
    main()