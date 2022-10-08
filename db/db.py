"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import json
import requests
import os

MONGODB_API_KEY = os.getenv("MONGODB_API_KEY")

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


def POST(operation, doc):
    """
    A multipurpose function for POST methods to the MongoDB
    Atlas Data API. This should be split into several other
    functions, methinks.
    """
    if operation == "findOne" or operation == "deleteOne":
        docType = "filter"
    else:
        docType = "document"

    url = ("https://data.mongodb-api.com"
           "/app/data-gvhux/endpoint/data"
           "/v1/action/{}"
           .format(operation))

    payload = json.dumps({
        "collection": "events",
        "database": "ticketScraper",
        "dataSource": "Cluster08493",
        docType: doc
    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': (MONGODB_API_KEY),
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    if "error" in response_json:
        raise Exception(f"{response_json['error']}")
    return response_json


POST("insertOne", WALTER)
find = POST("findOne", FIND_ALAN)
print(isinstance(find["document"], dict))
POST("findOne", FIND_WALTER)
POST("deleteOne", FIND_WALTER)
POST("findOne", FIND_ALAN)
POST("findOne", FIND_WALTER)
