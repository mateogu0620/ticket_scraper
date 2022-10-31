from urllib import response
from requests import get
from dotenv import load_dotenv
import os

load_dotenv()

POSTAL_CODE = 'postal_code'
MAX_PRICE = "max_price"
START_DATE = "start_date"
END_DATE = "end_date"
SIZE = 'size'

# Ticketmaster
TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY')
TM_REQUIRED_EVENT_FIELDS = [POSTAL_CODE, MAX_PRICE, START_DATE, END_DATE, SIZE]

# SeatGeek
SEATGEEK_API_KEY = os.getenv('SEATGEEK_API_KEY')
SEATGEEK_API_SECRET = os.getenv('SEATGEEK_API_SECRET')

'''
Docs: 
    - https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#search-events-v2
    - https://platform.seatgeek.com/
'''

class Event:
    def __init__(self, name, url, sales, dates, classifications, priceRanges):
        self.name = name
        self.url = url
        self.sales = sales
        self.dates = dates
        self.classifications = classifications
        self.priceRanges = priceRanges
    
    def toDict(self):
        return {
            "name": self.name,
            "url": self.url,
            "sales": self.sales,
            "dates": self.dates,
            "classifications": self.classifications,
            "priceRanges":  self.priceRanges
        }

class SGEvent:
    def __init__(self, id_, name, type_, price, datetime, venue, url):
        # i hate using the _ but its pep-8 convention
        self.id_ = id_
        self.name = name
        self.type_ = type_
        self.price = price
        self.datetime = datetime
        self.venue = venue
        self.url = url
        # TODO genre

    def toDict(self):
        return {
            "id": self.id_,
            "name": self.name,
            "type": self.type_,
            "price": self.price,
            "datetime": self.datetime,
            "venue": self.venue,
            "url": self.url
        }

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
    TMQuery = (
        f"https://app.ticketmaster.com/discovery/v2/events?"
        f"apikey={TICKETMASTER_API_KEY}&"
        f"postalCode={postalCode}&"
        f"classificationName=music&"           # for pulling only musical events
        f"locale=*&"
        f"radius=30&"                          # search radius in miles (default 30mi)
        f"startDateTime={start_date}&"
        f"endDateTime={end_date}&"
        f"size={size}"                         # page size of response, defaults to 20
    )

    responseTM = get(TMQuery).json()

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
            # Assuming here that price ranges are specified for all events
            for ticket in e['priceRanges']:
                # if any of the ticket types lies under the max_price range,
                # we include that event in our filtered events return list
                if ticket['max'] <= max_price:
                    filtered_events.append(e)
                    break
        parsed_events = parseTicketmaster(filtered_events)
        return parsed_events


def seatgeekGetEvents(postal_code, max_price, start_date, end_date, size=20):
    '''
     Return a list of events from SeatGeek based in a US postal code
               !!! Dates MUST be in the formay YYYY-MM-DD !!!
    '''
    SGQuery =  (
        f"https://api.seatgeek.com/2/events?"
        f"geoip={postal_code}&"
        f"highest_price.lte={max_price}&"  # filter events by max ticket price 
        f"datetime_local.gte={start_date}&"  # filter events by date range
        f"datetime_local.lte={end_date}"  
    )

    responseSG = get(SGQuery, auth=(SEATGEEK_API_KEY, SEATGEEK_API_SECRET)).json()

    return makeAPICall(responseSG, size)

def makeAPICall(response, size):
    # If invalid API call
    if 'status' in response:
        raise Exception(f"{response['message']}")
    # If no events were found
    elif 'events' not in response:
        return []
    # If events were found
    else:
        return response['events'][:size]

def parseTicketmaster(events):
    # MGU: Not parsed yet, just setting up the parsing for now
    # This helps a lot for parsing: https://developer.ticketmaster.com/api-explorer/v2/
    # genre = ev['classifications'][0]['genre']['name']  # i.e Rock
    # subGenre = ev['classifications'][0]['subGenre']['name'] # i.e Classic Rock
    parsed_events = []
    for ev in events:
        p_ev = Event(ev['name'], ev['url'], ev['sales'], ev['dates'], ev['classifications'], ev['priceRanges'])
        parsed_events.append(p_ev.toDict())
    return parsed_events


def formatVenue(venue):
    """
    Formats SeatGeek venue field to a human-readable address
    """
    name = venue['name']
    address = venue['address'] + ' ' + venue['extended_address']
    return (name, address)

def formatDatetime(datetime):
    """
    Formats datetime field to a human-readable local date and time
    i.e. '2022-12-01T19:00:00' --> ('19:00', '2022-12-01')
    """
    date, time = dt.split('T')
    time = time[:-3]
    return (time, date)

def parseSeatGeek(apiRequests):
    events = {}
    for event in apiRequests:
        tracker = []
        tracker.append(event['id'])
        tracker.append(event['title'])
        tracker.append(event['type'])
        tracker.append(formatDatetime(event['datetime_local']))
        tracker.append(formatVenue(event['venue']))
        tracker.append(event['url'])
        events[tracker[0]] = tracker
    return events
