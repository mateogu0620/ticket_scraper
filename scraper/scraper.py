from requests import get

# API Keys (will eventually be stored as env variables so hopefully nobody else looks at this repo please?)
TICKETMASTER_API_KEY = "W41W8WQEjosIaqHVjoWJGDDdFbB9Begq"

testQuery = f"https://app.ticketmaster.com/discovery/v2/events?apikey={TICKETMASTER_API_KEY}&locale=*&size=1"
response = get(testQuery)

print(response.json())