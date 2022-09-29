"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import json
import requests

def fetch_pets():
    """
    A function to return all pets in the data store.
    """
    return {"tigers": 2, "lions": 3, "zebras": 1}

def api_post():
    url = "https://data.mongodb-api.com/app/data-gvhux/endpoint/data/v1/action/findOne"

    payload = json.dumps({
        "collection": "people",
        "database": "gettingStarted",
        "dataSource": "Cluster08493",
        "projection": {
            "_id": 1
        }
    })
    headers = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': 'Gyq0EYJvvC3z2bxJIY6b46HunN6LfqYlpXycSLEXPOYO77zOGmNvIRIUsQSqp44Y', 
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

api_post()



    
