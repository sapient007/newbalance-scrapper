# import libraries
from urllib import request
from bs4 import BeautifulSoup
import os
import json
import yagmail
import time
import sys
import datetime
import sys
import logging
import socket
from logging.handlers import SysLogHandler

#define some deafult paramerters
MODEL = os.getenv("MODEL", '860')
SIZE = os.getenv("SIZE", '9.5')
WIDTH = os.getenv("WIDTH", '2E')
TARGET_PRICE = os.getenv("PRICE", 60)
SLEEP_SEC = int(os.getenv("SLEEP_TIME_SEC", 43200)) #default to sleep for 12 hours
EMAIL = os.getenv("EMAIL", 'what@ever.com')
SMTP_USER = os.getenv("SMTP_USER") #no defaults are set for this 
SMTP_PASS = os.getenv("SMTP_PASS") #no defaults are set for this 
PAPER_TRAIL_EVENT = os.getenv("PAPER_TRAIL_EVENT", 11111)
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK", "https://hooks.slack.com/services/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")


print(PAPER_TRAIL_EVENT)

class ContextFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True

syslog = SysLogHandler(address=('logs.papertrailapp.com', int(PAPER_TRAIL_EVENT)))
syslog.addFilter(ContextFilter())

format = '%(asctime)s %(hostname)s NB_Scraper: %(message)s'
formatter = logging.Formatter(format, datefmt='%b %d %H:%M:%S')
syslog.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(syslog)
logger.setLevel(logging.INFO)

#log to sysout 
#logger.basicConfig(stream=sys.stdout, level=logging.DEBUG)

#start time
time_start = time.time()

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
    
    #print(price)
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
    logger.info("search started for " + MODEL + "/" + SIZE + "/" + WIDTH + " @ $" + str(TARGET_PRICE) + " with URL " + BASE_URL)
    send_to_slack("search started for " + MODEL + "/" + SIZE + "/" + WIDTH + " @ $" + str(TARGET_PRICE) + " with URL " + BASE_URL)

    while True:
        try:
            # Check the page
            price = parse_page_for_price(BASE_URL)
            if price is not None:
                # Check the page
                if price <= TARGET_PRICE:
                    send_to_slack("@mling Price Mark Found at " + str(price) + " with URL " + BASE_URL)
                    #price is > than target
                else:
                    logger.info("lowest price > target " + str(price) )
                    send_to_slack("price at " + str(price)) 
            else:
                logger.info("nothing found. lowest price is " + str(price) )
                #send_to_slack("nothing found")
            
            logger.info("Going to sleep for " +  str(datetime.timedelta(seconds=SLEEP_SEC)) + " hours" )
            
            slept = 0 
            logger.info("going to sleep... " + str(slept) + " secs have past" )

            while (slept < SLEEP_SEC):
                slept += 1800
                time.sleep(1800)
                logger.info("sleeping ... still sleeping... " + str(slept) + " secs have past " +  str(SLEEP_SEC-slept) + " seconds remain for the next scan")
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    # TODO: Run scheduler once a day
    main()
