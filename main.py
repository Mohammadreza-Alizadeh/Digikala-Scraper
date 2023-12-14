from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from time import sleep
import csv
from datetime import datetime
import random
import re

# Main Domain
URL = r'https://www.digikala.com/search/'

def get_product_from_user():
    
    # A simple loop until user type a actual input
    while True:
        if product := input('Enter The Product you want to search for: ').strip():
            return product 


def make_url(product_slug, page_num=1):
    
    # creating URL for a specific page and product
    return (f'{URL}/?page={page_num}&q={product_slug}/' , page_num + 1)
    
def check_not_found():
    
    # check if there is no product on page
    try:
        driver.find_element(By.CLASS_NAME, 'styles_NotFound__image__LRvmi')
        return True
    except :
        return False


def is_page_end():
    
    # a simple javascript wich checks if we are at the bottom of the page
    return driver.execute_script("return (window.innerHeight + window.pageYOffset) >= document.body.scrollHeight - 10")


def scroll_to_end_of_page():
    
    # a loop wich sends SPACE to page so the page scrolls
    # it continus until reach the bottom of the page  
    while True:
        page = driver.find_element(By.TAG_NAME , 'html')
        page.send_keys(Keys.SPACE)
        if is_page_end():            
            return page
        sleep(0.2)
    
def collect_data(file_name):

    # create Soup Object so we can analyse
    soup = BeautifulSoup(driver.page_source , 'html.parser')
    
    # find all the products HTML cards and put them in list
    products = soup.find_all('div', class_='product-list_ProductList__item__LiiNI')
    
    # checks if there is no product
    if len(products) == 0 :
        return -1
    
    # opens the csv file 
    with open(file_name + '.csv', 'a', encoding='utf-8') as f:
        
        fieldnames = ['title', 'price']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # iterate to products and find data in each card and insert them to csv file
        for product in products:
            title = product.find('h3', class_ ='ellipsis-2 text-body2-strong text-neutral-700 styles_VerticalProductCard__productTitle__6zjjN')
            price = product.select_one('a > div > article > div.flex.grow.relative.flex-col > div.grow.flex.flex-col.items-stretch.justify-start > div.pt-1.flex.flex-col.items-stretch.justify-between > div:nth-child(1) > div > span')
            writer.writerow({'title':title.text, 'price':price.text}) 
            

def get_file_name():

    
    inp = input('your data will be saved in a CSV file\nEnter file name (without .csv at the end): ')
    # loop until user provide a valid file name  
    while not is_valid_file_name(inp):
        inp = input('your given name is not valid ( used illegal chars or a name that used already ): ')
    
    return inp



def is_valid_file_name(file_name):
    
    ILLEGAL_CHARS = r'[<>:"/\\|?*\x00-\x1F]'


    # Check for forbidden characters
    if re.search(ILLEGAL_CHARS, file_name):
        return False

    # Check for reserved names
    RESERVED_NAMES = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
    if file_name.upper() in RESERVED_NAMES:
        return False

    # Check for empty name
    if not file_name.strip():
        return False

    # Check for names starting or ending with dot or space
    if file_name.startswith('.') or file_name.endswith('.') or file_name.startswith(' ') or file_name.endswith(' '):
        return False

    # Check for names longer than 255 characters
    if len(file_name) > 255:
        return False

    
    # Check if it's name is already exist | it's important to not to append to an existed file 
    ALREADY_EXIST_FILE_NAMES =  [os.path.splitext(name)[0] for name in os.listdir() if os.path.splitext(name)[1] == '.csv']
    if file_name in ALREADY_EXIST_FILE_NAMES:
        return False    

    # All checks passed
    return True


def open_file_for_first_time(file_name):
    with open(file_name + '.csv', 'a', encoding='utf-8') as f:
        fieldnames = ['title', 'price']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()


def main(product, file_name):
    # initial url 
    url, new_page_num = make_url(product) 
    
    # open first page
    driver.get(url)
    
    # close the program if there is no product for user input
    if check_not_found():
        print('there is no result for your input !!!') # Log 
        return    
    
    while True:
        scroll_to_end_of_page()
        if collect_data(file_name) is not None:
            break
        new_url, new_page_num = make_url(product, new_page_num) 
        driver.get(new_url)
        sleep(2.0)

        

product = get_product_from_user()
file_name = get_file_name() 
driver = webdriver.Chrome()
driver.maximize_window()
open_file_for_first_time(file_name)
main(product, file_name)


