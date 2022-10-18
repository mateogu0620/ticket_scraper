#!/usr/bin/python3

from requests import get, auth
from json import loads, dumps

CLIENT_ID = "Mjk0MDI2MjJ8MTY2NDM5OTMyMi40MTQzNTQ"   # SeatGeek CLIENT_ID
endpoint_url = "https://api.seatgeek.com/2/genres"  # genres endpoint for SeatGeek API
url_auth = auth.HTTPBasicAuth(CLIENT_ID,"") # authorization, no pw

# for making an arbitrary SeatGeek API call
'''
    Since all possible genres are listed at the /genres endpoint URL, we must
    make an API call to that endpoint to return the value of every possible genre.
    The same concept works for other endpoints listed at https://platform.seatgeek.com
'''
def api_call(url, auth):
    # GET data
    res = get(url=url, auth=auth)

    # if error 
    if res.status_code != 200:
        print("ERROR!")
        return

    # parse and format response in JSON
    parsed_json = loads(res.content)
    #formatted_json = dumps(parsed_json, indent=4)
    #print(formatted_json)
    for i in range(len(parsed_json['genres'])):
        print(parsed_json['genres'][i]['name'])


api_call(endpoint_url, url_auth) # call API
