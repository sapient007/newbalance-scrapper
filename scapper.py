# import libraries
import urllib2
from bs4 import BeautifulSoup
import json
import yagmail

#define some seach basic paramerters
MODEL = '860'
SIZE = '9.5'
WIDTH = 'W'
TARGET_PRICE = '50'
EMAIL = ''

# specify the url
BASE_URL= ''

def generateBaseURL():
    BASE_URL = 'https://www.joesnewbalanceoutlet.com/products/?Filters%5BSize%5D=9.5&Filters%5BWidth%5D=W&PriceRange=&OnSale=&Icon=&Brand=0&PageSize=24&Page=1&Branded=False&ListType=Grid&Text=860&Sorting=Newest'

def parsePage():
    page = urllib2.urlopen(quote_page)
    soup = BeautifulSoul(page, 'html.parser')
    #check to see if shoes are below the target price <to be implemented>


def notify():
    yag = yagmail.SMTP()
    contents = ['found you a cheap shoe, here is the link' BASE_URL ]
    yag.send(EMAIL, 'new balance found', contents)

