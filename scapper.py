# import libraries
from urllib import request
from bs4 import BeautifulSoup
import os
import json
import yagmail
import time
import sys
import datetime
import logging
import sys

#log to sysout 
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

#start time
time_start = time.time()

#Slack Channel Webhook
SLACK_WEBHOOK = "https://hooks.slack.com/services/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"

#define some deafult paramerters
MODEL = os.getenv("MODEL", '860')
SIZE = os.getenv("SIZE", '9.5')
WIDTH = os.getenv("WIDTH", '2E')
TARGET_PRICE = os.getenv("PRICE", 60)
SLEEP_SEC = int(os.getenv("SLEEP_TIME_SEC", 43200)) #default to sleep for 12 hours
EMAIL = os.getenv("EMAIL", 'what@ever.com')
SMTP_USER = os.getenv("SMTP_USER") #no defaults are set for this 
SMTP_PASS = os.getenv("SMTP_PASS") #no defaults are set for this 

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

#email alerts
# TODO: not fully implemented
def notify_me():
    yag = yagmail.SMTP()
    contents = ['found you a cheap shoe, here is the link' + BASE_URL ]
    yag.send(EMAIL, 'new balance found', contents)


#send a message to slack 
def send_to_slack(price):
    post = {"text": "{0}".format(price)}
    try:
        json_data = json.dumps(post)
        req = request.Request(SLACK_WEBHOOK,
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'}) 
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))
    
def main():
    #initalize application
    send_to_slack("search started for " + MODEL + "/" + SIZE + "/" + WIDTH + " @ $" + str(TARGET_PRICE) + " with URL " + BASE_URL)

    while True:
        try:
            # Check the page
            price = parse_page_for_price(BASE_URL)
            if price is not None:
                # Check the page
                if price < TARGET_PRICE:
                    send_to_slack("@mling Price Mark Found at " + str(price) + " with URL " + BASE_URL)
            else:
                send_to_slack("nothing found")
            logging.info("Going to sleep for " +  str(datetime.timedelta(seconds=SLEEP_SEC)) + " hours" )
            time.sleep(SLEEP_SEC)
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    # TODO: Run scheduler once a day
    main()
