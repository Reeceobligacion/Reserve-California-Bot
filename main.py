#! /usr/bin/env python3

import time
import logging
import config as authkeys
import selenium.webdriver as webdriver
from bs4 import BeautifulSoup
from twilio.rest import Client

'''
AIM -> Checks the Pfieffer Big Sur campsites on the Reserve California website and sends us a text notification when availability is found
INPUT ->  Currently no inputs
OUTPUT -> Either a text notification that a campsite is available or recursively call the program in an hour
'''

# Configuration for target site and launch using Selenium
target_website = "https://www.reservecalifornia.com/CaliforniaWebHome/"
browser = webdriver.Chrome(executable_path="/Users/reece/downloads/chromedriver")
browser.get(target_website)

# Configuration for script logging
logging.basicConfig(filename='actions.log', level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

# Function for sending SMS message with Twilio
def sendtext(message):
    twilioCli = Client(authkeys.accountSID, authkeys.authToken)
    twilioCli.messages.create(body=message, from_=authkeys.twilioNumber, to=authkeys.myNumber)

# Find a specific park
# Reserve California requires you to select the specific park from the autocomplete list, otherwise results to filler text
search_box_main = browser.find_element_by_id("txtSearchparkautocomplete")
search_box_main.send_keys("pfe")
time.sleep(2)
auto_complete = browser.find_element_by_partial_link_text('Big Sur')
auto_complete.click()

# Find the specific date
search_box_date = browser.find_element_by_id("mainContent_txtArrivalDate")
search_box_date.click()
search_box_date.send_keys("09/22/2019")

# Find the stay length
search_box_length = browser.find_element_by_id("ddlHomeNights")
search_box_length.send_keys("1")

# Submit the form
search_box_go = browser.find_element_by_link_text("Search")
search_box_go.click()

# Access the web contents with beautiful soup
web_contents = BeautifulSoup(browser.page_source, 'html.parser')
target_div = web_contents.find("div", {"class": "FirstBlock"})

# Action logic when we find an availability
# Searches for the green checkmark icon within the FirstBlock div
try:
    if target_div.findAll("span", {"class": "full_green_clr"}):
        print("There is an available campsite")
        sendtext('Found an available campsite for Pfeiffer Big Sur, please book now')
        logging.info('Found an available campsite')
    elif target_div.findAll("span", {"class": "full_red_clr"}):
        # Rerun the application in an hour
        print("There are no availabilities")
        logging.info('No available campsites')
    else:
        sendtext('Could not find the proper content value, please review script')
        print("There was an error")
        logging.info('There was an error')
except AttributeError:
    sendtext('There was a runtime error, please review script')
    logging.info('There was an error, re-run the script')

browser.quit()
