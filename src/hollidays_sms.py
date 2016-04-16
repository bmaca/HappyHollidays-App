# Author     Bill Maca

import datetime
import ConfigParser
import os
import time
import holidays
from twilio.rest import TwilioRestClient

today = datetime.date.today()

# Reading sensitive credentials in order to communicate with twilio api
config = ConfigParser.ConfigParser()
home = os.path.join(os.path.expandvars("$HOME"), ".credentials.txt")
config.read(home)

# Declaring the Twilio creds in order to communiate with their API
TWILIO_ACCOUNT_SID = config.get("credentials","ACCOUNT_SID")
TWILIO_ACCOUNT_AUTH_TOKEN = config.get("credentials","AUTH_TOKEN")

# twilio generates a phone number for you
my_number = '+xxx'

# body of the message. Yall folks can change it to whatever you please. 
body = "Happy holidays to you and your family! From{}".format(name)

# reading the contacts from a file and converting them to a list. 
recipients = open('phone_numbers.txt').read().split('\n')

# create the client connection to the api
client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_AUTH_TOKEN)


def request():
    """
    Twilio requires you to make seperate REST api calls
    to the list of phone numbers that you will want to send to
    so the best way is to iterate over an array of recipients.
    """
    for contacts in recipients:
        # added this because I didnt want to abuuse their api server
        time.sleep(1)
        client.messages.create(
                to=contacts,
                from_=my_number,
                body=body)

def us_hollidays(year):
    for date in sorted(holidays.US( years=year).items()):
        if date == today:
            request()
        else:
            pass
# client can pass in any year they want
us_hollidays(year)

def easter(year, _type):
    """ 
    Retrieve the respected easter hollidays. 
    Supply a year and a _type.  There are only 3 types: easter_julian,
    easter_orthodox, easter_western
    """
    if _type == "eastern_julian" and holidays.easter(year=year, method=1) == today:
        request()

    elif _type == "easter_orthodox" and holidays.easter(year=year, method=2) == today:
        request()

    else:
        if _type == "easter_western" and holidays.easter(year=year, method=3) == today:
            request()

# client can pass in the year and type of easter
easter(year, _type)



