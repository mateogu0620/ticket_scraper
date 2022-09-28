from requests import get

'''
API Keys (will eventually be stored as env variables so hopefully nobody else looks at this repo please?)

Docs: 
    - https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/#search-events-v2
    - https://platform.seatgeek.com/
    -

'''

# Ticketmaster
TICKETMASTER_API_KEY = "W41W8WQEjosIaqHVjoWJGDDdFbB9Begq"
# SeatGeek
SEATGEEK_CLIENTID = "Mjk0MDI2MjJ8MTY2NDM5OTMyMi40MTQzNTQ"
SEATGEEK_SECRET = "ef42c7b4250a963a18a8f42fcb817bcdc3c2889e8740ac276b6834f48df45275"
SEATGEEK_AUTH = f"client_id={SEATGEEK_CLIENTID}&client_secret={SEATGEEK_SECRET}"

# Examples for searching events using all three APIs - refer to docs for more info
testTMQuery = f"https://app.ticketmaster.com/discovery/v2/events?apikey={TICKETMASTER_API_KEY}&locale=*&size=1"
testSGQuery = f"https://api.seatgeek.com/2/events?geoip=11201"

print(testSGQuery)



responseTM = get(testTMQuery)
responseSG = get(testSGQuery, auth=(SEATGEEK_CLIENTID, SEATGEEK_SECRET))

print(responseTM.json())
print(responseSG.json())