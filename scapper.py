# import libraries
from urllib import request
from bs4 import BeautifulSoup
import json
import yagmail

#define some seach basic paramerters
MODEL = '1080'
SIZE = '9.5'
WIDTH = '2E'
TARGET_PRICE = 50
EMAIL = ''

# specify the url
BASE_URL= 'https://www.joesnewbalanceoutlet.com/men/shoes/running/?Filters%5BSize%5D=' + SIZE + '&Filters%5BWidth%5D=' + WIDTH + '&Categories=men&Categories=shoes&Categories=running&PriceRange=&OnSale=&Icon=&Brand=0&PageSize=24&Page=1&Branded=False&ListType=Grid&Text=' + MODEL + '&Sorting=LowestPrice'

def parse_page_for_price(quote_page):
    page = request.urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')
    #scape the screen and find the lowest price posted
    # TODO: add a condition there if no results are found in the search
    price_div = soup.find('div', attrs={'class': 'productPrice'})
    if price_div is not None:
        price = price_div.text.strip().replace("$", "")
    else:
        return
    
    print(price)
    return float(price)


def notify_me():
    yag = yagmail.SMTP()
    contents = ['found you a cheap shoe, here is the link' + BASE_URL ]
    yag.send(EMAIL, 'new balance found', contents)


def main():
    # Check the page
    price = parse_page_for_price(BASE_URL)
    if price is not None:
        # Check the page
        if price < TARGET_PRICE:
            notify_me()

if __name__ == "__main__":
    # TODO: Run scheduler once a day
    main()