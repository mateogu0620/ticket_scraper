"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import json
import requests
import os
from pymongo import MongoClient
from scraper import scraper

MONGODB_API_KEY = os.getenv("MONGODB_API_KEY")
MONGODB_TOGGLE = os.getenv("MONGODB_TOGGLE")

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


def local_POST(operation, doc):
    connectionString = "mongodb://localhost:27017/"
    client = MongoClient(connectionString)
    db = client['ticketScraper']
    collection = db['events']

    if operation == "findOne":
        result = collection.find_one(doc)
        result.pop("_id")
        return {"document": result}
    elif operation == "find":
        results = collection.find(doc)
        for ev in results:
            ev.pop("_id")
        return {"documents": results}
    elif operation == "deleteOne":
        return {"deletedCount": collection.delete_one(doc).deleted_count}
    elif operation == "deleteMany":
        return {"deletedCount": collection.delete_many(doc).deleted_count}
    elif operation == "insertOne":
        return {"insertedId": str(collection.insert_one(doc)
                                            .inserted_id)
                }
    elif operation == "insertMany":
        return {"insertedIds": [str(i) for
                                i in collection.insert_many(doc)
                                               .inserted_ids]
                }


def POST(operation, doc):
    """
    A multipurpose function for POST methods to the MongoDB
    Atlas Data API. This should be split into several other
    functions, methinks.
    """
    if operation == "findOne" or \
       operation == "deleteOne" or \
       operation == "find" or \
       operation == "deleteMany":
        docType = "filter"
    elif operation == "insertMany":
        docType = "documents"
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


def convertToEvent(events):
    converted = []
    for e in events:
        converted.append(scraper.Event(
            e["provider"],
            e["id"],
            e["name"],
            e["url"],
            e["venueName"],
            e["venueAddress"],
            e["eventDate"],
            e["eventTime"],
            e["genre"],
            e["minPrice"],
            e["maxPrice"],
        ))
    return converted


def insertManyTicketmaster(filter):
    operation = "insertMany"
    events = scraper.ticketmasterGetEvents(filter['postalCode'],
                                           filter['maxPrice'],
                                           filter['start_date'],
                                           filter['end_date'],
                                           filter['size'])
    return POST(operation, events)


POST("insertOne", WALTER)
find = POST("findOne", FIND_ALAN)
print(isinstance(find["document"], dict))
POST("findOne", FIND_WALTER)
POST("deleteOne", FIND_WALTER)
POST("findOne", FIND_ALAN)
POST("findOne", FIND_WALTER)
