from urllib import response
from requests import get
from dotenv import load_dotenv
import os

load_dotenv()

# Ticketmaster
TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY')
# SeatGeek
SEATGEEK_API_KEY = os.getenv('SEATGEEK_API_KEY')
SEATGEEK_API_SECRET = os.getenv('SEATGEEK_API_SECRET')


'''
Docs: 
    - https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#search-events-v2
    - https://platform.seatgeek.com/
'''


def ticketmasterGetEvents(size, postalCode):
    '''
    Return a list of events from Ticketmaster based in a US postal code

    MGU: still some work pending in checking for edge cases and handling
    what is the max size we are allowing (TM allows for 200, but it is very
    slow)
    '''
    testTMQuery = (
        f"https://app.ticketmaster.com/discovery/v2/events?"
        f"apikey={TICKETMASTER_API_KEY}&"
        f"postalCode={postalCode}&"
        f"locale=*&"
        f"size={size}"
    )

    responseTM = get(testTMQuery).json()

    # If API call failed
    if 'errors' in responseTM:
        raise Exception("Invalid API call")
    # If API stops working for some reason
    elif 'fault' in responseTM:
        raise Exception("Invalid API credentials")
    # If no events were found
    elif '_embedded' not in responseTM:
        return []
    # If events were found
    else:
        return responseTM['_embedded']['events']


def seatgeekGetEvents(size, postalCode):
    '''
    Return a list of events from SeatGeek based in a US postal code 
    '''
    testSGQuery =  (
        f"https://api.seatgeek.com/2/events?"
        f"geoip={postalCode}"
    )
    
    responseSG = get(testSGQuery, auth=(SEATGEEK_API_KEY, SEATGEEK_API_SECRET)).json()

    # If invalid API call
    if 'status' in responseSG:
        raise Exception(f"{responseSG['message']}")
    # If no events were found
    elif 'events' not in responseSG:
        return []
    # If events were found
    else:
        return responseSG['events'][:size]