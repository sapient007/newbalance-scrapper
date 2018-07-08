# import libraries
import urllib2
from bs4 import BeautifulSoup
import json
import yagmail

#define some seach basic paramerters
#MODEL = '860'
#SIZE = '9.5'
#WIDTH = 'W'
TARGET_PRICE = '50'
EMAIL = ''

# specify the url
BASE_URL= ''

def generateBaseURL():
    BASE_URL = 'https://www.joesnewbalanceoutlet.com/men/shoes/running/?Filters%5BSize%5D=9.5&Filters%5BWidth%5D=2E&Categories=men&Categories=shoes&Categories=running&PriceRange=&OnSale=&Icon=&Brand=0&PageSize=24&Page=1&Branded=False&ListType=Grid&Text=1080&Sorting=LowestPrice'

def parse_page_for_price(quote_page):
    page = urllib2.urlopen(quote_page)
    soup = BeautifulSoul(page, 'html.parser')
    #scape the screen and find the lowest price posted
    price_div = soup.find('div', attrs={'class': 'productPrice'})
    price = price_div.text.strip()
    print price
    return price


def notify_me():
    yag = yagmail.SMTP()
    contents = ['found you a cheap shoe, here is the link' BASE_URL ]
    yag.send(EMAIL, 'new balance found', contents)


def main()
    # Check the page
    price = parse_page_for_price()

    # Check the page
    if price < threshold_price:
        notify_me()


if __name__ == "__main__":
    # TODO: Run scheduler once a day
    main()
