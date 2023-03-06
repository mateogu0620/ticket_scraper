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
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
"""
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
"""

MONGODB_API_KEY = os.getenv("MONGODB_API_KEY")
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']


def fetch_pets():
    """
    A function to return all pets in the data store.
    """
    return {"tigers": 2, "lions": 3, "zebras": 1}


def set_credentials():
    client_id = os.getenv("OAUTH_CLIENT_ID")
    client_secret = os.getenv("OAUTH_CLIENT_SECRET")
    form = {
        "web": {
            "client_id": f"{client_id}",
            "project_id": "ticket-scraper-379001",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url":
            "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": f"{client_secret}"
        }
    }
    return form


def POST(operation, collection, doc):
    connectionString = os.getenv("MG_CONNECTION_STRING")
    client = MongoClient(connectionString)
    db = client['ticketScraper']
    collection = db[collection]

    if operation == "findOne":
        result = collection.find_one(doc)
        if result is not None:
            result.pop("_id")
        return {"document": result}
    elif operation == "find":
        results = list(collection.find(doc))
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


def login():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    else:
        return {"message": "Valid OAuth token!"}
    """
    try:
        service = build('people', 'v1', credentials=creds)
        # Call the People API
        print('List 10 connection names')
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=10,
            personFields='names,emailAddresses').execute()
        connections = results.get('connections', [])
        for person in connections:
            names = person.get('names', [])
            if names:
                name = names[0].get('displayName')
                print(name)
    except HttpError as err:
        print(err)
    """


def api_POST(operation, doc):
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
