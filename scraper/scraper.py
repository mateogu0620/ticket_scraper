from requests import get
from dotenv import load_dotenv
import os

load_dotenv()

POSTAL_CODE = 'postal_code'
MAX_PRICE = "max_price"
START_DATE = "start_date"
END_DATE = "end_date"
SIZE = 'size'
SG_GENRES = ['Country', 'Pop', 'Rock', 'Alternative', 'Indie', 'Punk', 'Blues', 'Soul',
             'Folk', 'Jazz', 'Reggae', 'Classic Rock', 'Hard Rock', 'Electronic', 'Rnb',
             'Hip-Hop', 'Rap', 'Funk', 'Latin', 'Classical', 'Techno']

# List is not exhaustive!
TM_GENRES = ['Alternative', 'Blues', 'Theatre', 'Classical', 'Comedy', 'Country', 'Dance',
             'Family', 'Festivals','Hip-Hop/Rap',  'Jazz', 'Latin','Miscellaneous', 'Musicals',
             'New Age', 'Opera', 'Pop', 'R&B/Soul', 'Reggae', 'Rock', 'Sports', 'Soul', 'Hip-Hop',
             'Rap', 'R&B', 'Funk', 'Electronic', 'Folk', 'Punk', 'Indie'] # Hard Rock, Metal ? 

# Ticketmaster
TICKETMASTER_API_KEY = os.getenv('TICKETMASTER_API_KEY')
TM_REQUIRED_EVENT_FIELDS = [POSTAL_CODE, MAX_PRICE, START_DATE, END_DATE, SIZE]

# SeatGeek
SEATGEEK_API_KEY = os.getenv('SEATGEEK_API_KEY')
SEATGEEK_API_SECRET = os.getenv('SEATGEEK_API_SECRET')


class Event:
    def __init__(self, provider, id_, name, url, venueName, venueAddress, eventDate, eventTime, genre, minPrice, maxPrice):
        # provider: a string, either 'tm' or 'sg' to indicate where it comes from
        # events will be identified by their provider AND the event id
        self.provider = provider
        self.id_ = id_
        self.name = name
        self.url = url
        self.venueName = venueName
        self.venueAddress = venueAddress
        self.eventDate = eventDate
        self.eventTime = eventTime
        self.genre = genre
        self.minPrice = minPrice
        self.maxPrice = maxPrice

    def toDict(self):
        return {
            "provider": self.provider,
            "id": self.id_,
            "name": self.name,
            "url": self.url,
            "venueName": self.venueName,
            "venueAddress": self.venueAddress,
            "eventDate": self.eventDate,
            "eventTime": self.eventTime,
            "genre": self.genre,
            "minPrice": self.minPrice,
            "maxPrice": self.maxPrice
        }


def getEvents(postal_code, max_price, start_date, end_date, size):
    '''
    Returns a list of the combined Events from Ticketmaster and Seatgeek
    '''
    # split the size as evenly as possible among both API calls
    if size % 2 == 0:
        tmsize = sgsize = size // 2
    else:
        # if the size is an odd number, SeatGeek will have to return 
        # one more event than Ticketmaster
        tmsize = size // 2
        sgsize = (size // 2) + 1

    tmEvents = ticketmasterGetEvents(postal_code, max_price, start_date, end_date, tmsize)
    sgEvents = seatgeekGetEvents(postal_code, max_price, start_date, end_date, sgsize)

    events = tmEvents + sgEvents

    return events


def ticketmasterGetEvents(postal_code, max_price, start_date, end_date, size, genre="music"):
    '''
    Return a list of TMEvent objects from the Ticketmaster API
    '''
    if genre is None or genre not in TM_GENRES:
        genre = "music"

    TMQuery = (
        f"https://app.ticketmaster.com/discovery/v2/events?"
        f"apikey={TICKETMASTER_API_KEY}&"
        f"postalCode={postal_code}&"
        f"classificationName={genre}&"           # for pulling only musical events
        f"locale=*&"
        f"radius=30&"                          # search radius in miles (default 30mi)
        f"localstartDateTime={start_date}&"
        f"localendDateTime={end_date}&"
        f"size={size}"
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
            # Check if a venue is specified
            if not e['_embedded']['venues']:
                e['venues'] = {}
            else:
                e['venues'] = e['_embedded']['venues']
            try:
                for ticket in e['priceRanges']:
                    # if any of the ticket types lies under the max_price range,
                    # we include that event in our filtered events return list
                    if ticket['max'] <= max_price:
                        filtered_events.append(e)
                        break
            except:
                # Handle scenario where price ranges is not specified
                e['priceRanges'] = [{"min": None, "max": None}]
                filtered_events.append(e)
        parsed_events = parseTicketmasterEvents(filtered_events)
        return parsed_events


def seatgeekGetEvents(postal_code, max_price, start_date, end_date, size=20, genre=None):
    '''
     Return a list of events from SeatGeek based in a US postal code
               !!! Dates MUST be in the formay YYYY-MM-DD !!!
    '''
    SGQuery =  (
        f"https://api.seatgeek.com/2/events?"
        f"geoip={postal_code}&"
        f"highest_price.lte={max_price}&"  # filter events by max ticket price 
        f"datetime_local.gte={start_date}&"  # filter events by date range
        f"datetime_local.lte={end_date}&"
        f"type=concert"          # only filter concert tickets, could possibly 
                                 # change to include musicals, etc
    )
    if genre is not None and genre in SG_GENRES:
        SGQuery += f"&taxonomies.name={genre}" # filter events by genre

    responseSG = get(SGQuery, auth=(SEATGEEK_API_KEY, SEATGEEK_API_SECRET)).json()

    events =  makeAPICall(responseSG, size)
    parsed_events = parseSeatGeek(events)
    return parsed_events

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

def parseTicketmasterEvents(events):
    # Resource for parsing: https://developer.ticketmaster.com/api-explorer/v2/
    parsed_events = []
    for ev in events:
        # name, location/venue, dates, pirce, url, genre
        eventID = ev['id']
        eventName = ev['name']
        eventUrl = ev['url']
        venueName, venueAddress = formatVenue('tm', ev['venues']) if ev['venues'] else ("Not specified", "Not specified")
        eventTime, eventDate = formatDatetime('tm', ev['dates'])
        genre = ev['classifications'][0]['genre']['name']
        minPrice, maxPrice = ev['priceRanges'][0]['min'], ev['priceRanges'][0]['max']
        p_ev = Event("tm",
                       eventID,
                       eventName,
                       eventUrl,
                       venueName,
                       venueAddress,
                       eventDate,
                       eventTime,
                       genre,
                       minPrice,
                       maxPrice
        )
        parsed_events.append(p_ev)
    return parsed_events

'''
def parseDates(dates):
    localDate = dates['start']['localDate']
    localTime = dates['start']['localTime']
    return localDate, localTime
'''

def parseSeatGeek(events):
    parsed_events = []
    for e in events:
        try:
            # sometimes genre field is not provided
            genre = e['performers'][0]['genres'][0]["name"]
        except:
            genre = None
        
        venue = formatVenue('sg', e['venue'])
        datetime = formatDatetime('sg', e['datetime_local'])
        prices = formatPrices(e['stats'])
        concert = Event("sg", e['id'], e['title'], e['url'],
                               venue[0], venue[1], datetime[1], datetime[0],
                               genre, prices[0], prices[2])
        parsed_events.append(concert)
    return parsed_events

def formatVenue(provider, venue):
    """
        Formats TicketMaster and SeatGeek venue field to a human-readable address
          e.g. ('New York Theatre Workshop', '721 Broadway New York, NY 10003')
    """
    if provider == 'tm':
        venue = venue[0]
        name = venue['name']
        city = venue['city']['name']
        state = venue['state']['stateCode'].strip()
        try:
            address = f"{venue['address']['line1']} {city}, {state} {venue['postalCode']}"
        except KeyError:
            address = f"{venue['address']} {city}, {state} {venue['postalCode']}"

    elif provider == 'sg':
        name = venue['name']
        if not venue['address']:
            return (name, 'Address not found')
        if not venue['extended_address']:
            return (name, venue['address'])

        address = venue['address'] + ' ' + venue['extended_address']

    else:
        raise Exception("Invalid provider.")

    return (name, address)

def formatPrices(prices):
    """
    Formats SeatGeek stats dict into a tuple of price information
    in the following format:
    ->    (lowest_price, average_price, highest_price)
    """
    lowest_price = prices['lowest_price']
    avg_price = prices['average_price']
    highest_price = prices['highest_price']

    if (not lowest_price and not avg_price and not highest_price):
        # if no price data is found
        return (None, None, None)
    
    return (lowest_price, avg_price, highest_price)


def formatDatetime(provider, datetime):
    """
    Formats datetime field to a unified human-readable local date and time
    e.g. '2022-12-01T19:00:00' --> ('19:00', '2022-12-01')
    """
    
    if provider == 'tm':
        date = datetime['start']['localDate']
        try:
            time = datetime['start']['localTime']
        except KeyError:
            time = 'N/A'
        return (time, date)

    elif provider == 'sg':
        date, time = datetime.split('T')
        time = time[:-3]
        return (time, date)
