from urllib import response
from requests import get
from dotenv import load_dotenv
import os

load_dotenv()

# Ticketmaster
TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY')
TM_POSTAL_CODE = 'postal_code'
TM_MAX_PRICE = "max_price"
TM_START_DATE = "start_date"
TM_END_DATE = "end_date"
TM_SIZE = 'size'
TM_REQUIRED_EVENT_FIELDS = [TM_POSTAL_CODE, TM_MAX_PRICE, TM_START_DATE, TM_END_DATE, TM_SIZE]
# SeatGeek
SEATGEEK_API_KEY = os.getenv('SEATGEEK_API_KEY')
SEATGEEK_API_SECRET = os.getenv('SEATGEEK_API_SECRET')


'''
Docs: 
    - https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#search-events-v2
    - https://platform.seatgeek.com/
'''

def ticketmasterGetEvents(postalCode, max_price, start_date, end_date, size):
    '''
    Return a list of events from Ticketmaster based in a US postal code

    start_date and end_date are in the format: %Y-%m-%dT%H:%M (e.g. 2019-01-01T00:00)
        - this is UTC time
    max_price is USD currency

    MGU: still some work pending in checking for edge cases and handling
    what is the max size we are allowing (TM allows for 200, but it is very
    slow)
    '''
    testTMQuery = (
        f"https://app.ticketmaster.com/discovery/v2/events?"
        f"apikey={TICKETMASTER_API_KEY}&"
        f"postalCode={postalCode}&"
        f"classificationName=music&"                        # for pulling only musical events
        f"locale=*&"
        f"radius=30&"                                       # search radius in miles (default 30mi)
        f"startDateTime={start_date}&"
        f"endDateTime={end_date}&"
        f"size={size}"                                      # page size of response, defaults to 20
    )

    responseTM = get(testTMQuery).json()

    # If API call failed
    if 'errors' in responseTM:
        print(responseTM)
        raise Exception("Invalid API call")
    # If API stops working for some reason
    elif 'fault' in responseTM:
        raise Exception("Invalid API credentials")
    # If no events were found
    elif '_embedded' not in responseTM:
        return []
    # If events were found
    else:
        events = responseTM['_embedded']['events']
        filtered_events = []
        for e in events:
            for ticket in e['priceRanges']:
                # if any of the ticket types lies under the max_price range,
                # we include that event in our filtered events return list
                if ticket['max'] <= max_price:
                    filtered_events.append(e)
                    break
        return filtered_events


def parseTicketMaster(apiRequests):
    events = {}
    for event in apiRequests:
        tracker = []
        tracker.append(event['id'])
        tracker.append(event['name'])
        tracker.append(event['type'])
        tracker.append(event['locate'])
        tracker.append(event['url'])
        tracker.append(event['price_range'])
        tracker.append(event['dates'])
        tracker.append(event['images'])
        events[tracker[0]] = tracker
    return events
    

def seatgeekFiltered(postalCode, max_price, start_date, end_date, size=20):
    '''
      Testing return of a list of events from SeatGeek based on certain user event filters
      !!! Dates MUST be in the format YYYY-MM-DD !!!
    '''
    testSGQuery =  (
        f"https://api.seatgeek.com/2/events?"
        f"geoip={postalCode}&"
        f"highest_price.lte={max_price}&"  # filter events by max ticket price ($20)
        f"datetime_local.gte={start_date}&"  # filter events by date
        f"datetime_local.lte={end_date}"  # -> returns all events in month of November
    )
    '''
       EVENT TYPE = 'concert' || 'band'  # figure out how to adapt filter for only musical events
       f"range=30"     # search radius in miles (default 30mi) # RETURNS invalid range: 30 why?
   ''' 

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

def parseSeatGeek(apiRequests):
    events = {}
    for event in apiRequests:
        tracker = []
        tracker.append(event['id'])
        tracker.append(event['title'])
        tracker.append(event['type'])
        tracker.append(event['venue'])
        tracker.append(event['url'])
        events[tracker[0]] = tracker
    return events
    