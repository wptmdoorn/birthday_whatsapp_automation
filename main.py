from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import os
import pandas as pd
import random
import re

CHROME_PROFILE_DIR = "C:/Users/Dealstunter/Desktop/Hobby projecten/birthday_whatsapp_automation/chrome_profile"

def _remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def get_birthdays() -> pd.DataFrame:
    # read contact list
    contacts = pd.read_csv('contacts.csv', sep=";")
    contacts['birthday'] = pd.to_datetime(contacts['birthday'], format='%d/%m/%Y')

    # Set Day for Comparison Using Today's DateTime
    today = pd.Timestamp.now().strftime('%m-%d')
    # Filter DataFrame
    return contacts.loc[contacts['birthday'].dt.strftime('%m-%d').eq(today)]


def get_random_message(relation_type: str) -> str:
    # load messages.json
    with open('messages.json') as f:
        messages = json.load(f)
        if relation_type not in messages.keys():
            print(f"Relation type {relation_type} not found in messages.json")
            print("Defaulting to friend")
            relation_type = "friend"

        return random.choice(messages[relation_type])



def send_message(contact: pd.Series) -> None:
    _first_time = not os.path.isdir(CHROME_PROFILE_DIR)
    _first_name = _remove_emoji(contact['firstname'].split(' ')[0])

    if _first_time:
        # make directory
        os.mkdir("./chrome_profile")

    options = webdriver.ChromeOptions() 
    options.add_argument(f'user-data-dir={CHROME_PROFILE_DIR}')
    
    if not _first_time:
        options.add_argument("--headless=new") # we can only do headless when we have a profile (and thus scanned QR code)

    driver = webdriver.Chrome(options=options)
    
    if _first_time:
        print('First time running, please scan QR code')
        baseurl = "https://web.whatsapp.com"
        driver.get(baseurl)
        #increase sleep time if your internet is slow or you need more time to scan,This is one time QR scan for sending 1 whole list
        time.sleep(20)


    # navigate to URL
    driver.get('https://web.whatsapp.com/send?phone=' + str(contact['phone']))
    time.sleep(20)
    
    # switch to active element and type message
    content = driver.switch_to.active_element
    message = get_random_message(contact['relation_type']).format(name=_first_name)
    content.send_keys(message)
    time.sleep(5)

    # press enter
    content.send_keys(Keys.RETURN)

    if ":" in message: # if any emoji's, we need to press enter twice
        time.sleep(5)
        content.send_keys(Keys.RETURN)
    
    # wait for message to be sent
    time.sleep(6)


if __name__ == "__main__":
    birthdays: pd.DataFrame = get_birthdays()

    for index, person in birthdays.iterrows():
        print(f"Sending message to {person['firstname']}")
        send_message(person)