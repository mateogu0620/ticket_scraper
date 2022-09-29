"""
This file will manage interactions with our data store.
At first, it will just contain stubs that return fake data.
Gradually, we will fill in actual calls to our datastore.
"""

import json
import requests
import datetime


def fetch_pets():
    """
    A function to return all pets in the data store.
    """
    return {"tigers": 2, "lions": 3, "zebras": 1}


def api_findOne(first, last):
    url = "https://data.mongodb-api.com/app/data-gvhux\
            /endpoint/data/v1/action/findOne"

    payload = json.dumps({
        "collection": "people",
        "database": "gettingStarted",
        "dataSource": "Cluster08493",
        'filter': {
            "name": {"first": first, "last": last}
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'Gyq0EYJvvC3z2bxJIY6b46HunN6LfqYlpXyc\
                    SLEXPOYO77zOGmNvIRIUsQSqp44Y',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def api_insertOne():
    url = "https://data.mongodb-api.com/app/data-gvhux/\
            endpoint/data/v1/action/insertOne"

    payload = json.dumps({
        "collection": "people",
        "database": "gettingStarted",
        "dataSource": "Cluster08493",
        "document": {
            "name": {
                "first": "Walter",
                "last": "White"
            },
            "birth": json.dumps(datetime.datetime.now(), indent=4,
                                sort_keys=True, default=str),
            "death": json.dumps(datetime.datetime.now(), indent=4,
                                sort_keys=True, default=str),
            "contribs": ["Jesse", "We", "Need", "To", "Cook"],
            "views": 5000000
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'Gyq0EYJvvC3z2bxJIY6b46HunN6LfqYlpXyc\
                    SLEXPOYO77zOGmNvIRIUsQSqp44Y',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


def api_deleteOne():
    url = "https://data.mongodb-api.com/app/data-gvhux/\
            endpoint/data/v1/action/deleteOne"

    payload = json.dumps({
        "collection": "people",
        "database": "gettingStarted",
        "dataSource": "Cluster08493",
        "filter": {"name": {"first": "Walter", "last": "White"}}
    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'Gyq0EYJvvC3z2bxJIY6b46HunN6LfqYlpXyc\
                    SLEXPOYO77zOGmNvIRIUsQSqp44Y',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)