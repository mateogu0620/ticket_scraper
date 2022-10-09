"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask
from flask_restx import Resource, Api
from scraper import scraper
from db import db

app = Flask(__name__)
api = Api(app)

''' #Shelving the client connection for now, pivoting to Data API

client = MongoClient('localhost', 27017)
# Username: Cluster08493
# Password: RlhRbmFKSH1E
db = client.flask_db  # creating mongoDB instance
collection = db.collec
'''

LIST = 'list'
HELLO = '/hello'
MESSAGE = 'message'
TM_GET_EVENTS = '/tm_get_events'
SG_GET_EVENTS = '/sg_get_events'
SG_FILTERS = '/sg_get_filtered_events'
MG_GET_DOCUMENT = '/mg_get_document'
MG_INSERT_DOCUMENT = '/mg_insert_document'
MG_DELETE_DOCUMENT = '/mg_delete_document'
EVENTS = 'events'
DOCUMENT = 'document'
INSERTED_ID = 'insertedId'
DELETED_COUNT = 'deletedCount'


@api.route(HELLO)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {MESSAGE: 'hello world'}


@api.route(f'{TM_GET_EVENTS}/<postalCode>')
class TMGetEvents(Resource):
    """
    Simple test to make sure the calls to Ticketmaster's GetEvents
    endpoint is working
    """
    def get(self, postalCode, size=20):
        """
        Calls Ticketmaster's API and return a list of events
        """
        events = scraper.ticketmasterGetEvents(postalCode, size)
        return {EVENTS: events}


@api.route(f'{SG_FILTERS}/<max_price>/<postalCode>/<start_date>/<end_date>')
class SGGetFilteredEvents(Resource):
    """
        Testing the filtering capacity of SeatGeek event calls
        !!! Dates MUST be in the format YYYY-MM-DD !!!
    """
    def get(self, postalCode, max_price, start_date, end_date, size=20):
        max_price = int(max_price)
        events = scraper.seatgeekFiltered(
            postalCode, max_price, start_date, end_date, size)
        return {EVENTS: events}


@api.route(f'{SG_GET_EVENTS}/<size>/<postalCode>')
class SGGetEvents(Resource):
    """
    Simple test to make sure the calls to SeatGeek's GetEvents
    endpoint is working
    """
    def get(self, size, postalCode):
        """
        Calls SeatGeek's API and return a list of events
        """
        # MGU: adding this for now until I figure out how to specify
        #      the types of the arguments using flask_restx
        size = int(size)
        events = scraper.seatgeekGetEvents(size, postalCode)
        return {EVENTS: events}


@api.route(f'{MG_INSERT_DOCUMENT}/<size>/<postalCode>')
class MGInsertDocument(Resource):
    """
    Test to make sure the MongoDB's Atlas Data
    API POST requests can add data
    """
    def get(self, size, postalCode):
        """
        Calls MongoDB's API and returns attributes of a doc
        """
        doc = {"size": size, "postalCode": postalCode}
        document = db.POST("insertOne", doc)
        return document


@api.route(f'{MG_GET_DOCUMENT}/<size>/<postalCode>')
class MGGetDocument(Resource):
    """
    Test to make sure the MongoDB's Atlas Data
    API POST request can find data
    """
    def get(self, size, postalCode):
        """
        Calls MongoDB's API and returns attributes of a doc
        """
        doc = {"size": size, "postalCode": postalCode}
        document = db.POST("findOne", doc)
        return document


@api.route(f'{MG_DELETE_DOCUMENT}/<size>/<postalCode>')
class MGDeleteDocument(Resource):
    """
    Test to make sure the MongoDB's Atlas Data
    API POST request can find data
    """
    def get(self, size, postalCode):
        """
        Calls MongoDB's API and returns attributes of a doc
        """
        doc = {"size": size, "postalCode": postalCode}
        document = db.POST("deleteOne", doc)
        return document
