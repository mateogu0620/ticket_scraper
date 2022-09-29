"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import json
import requests

WALTER = {
    "name": {
        "first": "Walter",
        "last": "White"
    },
    "birth": "eh",
    "death": "eh",
    "contribs": ["Jesse", "We", "Need", "To", "Cook"],
    "views": 5000000
}

FIND_ALAN = {"name": {"first": "Alan", "last": "Turing"}}
FIND_WALTER = {"name": {"first": "Walter", "last": "White"}}


def fetch_pets():
    """
    A function to return all pets in the data store.
    """
    return {"tigers": 2, "lions": 3, "zebras": 1}


def POST(operation, docType, doc):
    url = ("https://data.mongodb-api.com"
           "/app/data-gvhux/endpoint/data"
           "/v1/action/{}"
           .format(operation))

    payload = json.dumps({
        "collection": "people",
        "database": "gettingStarted",
        "dataSource": "Cluster08493",
        docType: doc
    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': ("Gyq0EYJvvC3z2bxJIY6b46HunN6L"
                    "fqYlpXycSLEXPOYO77zOGmNvIRIUsQSqp44Y"),
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


POST("insertOne", "document", WALTER)
POST("findOne", "filter", FIND_ALAN)
POST("findOne", "filter", FIND_WALTER)
POST("deleteOne", "filter", FIND_WALTER)
POST("findOne", "filter", FIND_ALAN)
POST("findOne", "filter", FIND_WALTER)
