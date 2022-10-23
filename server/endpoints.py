"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask, request
from flask_restx import Resource, Api, fields
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
MG_GET_MANY = '/mg_get_many'
MG_TM_INSERT = '/mg_tm_insert'
FILTER = 'filter'
EVENTS = 'events'
DOCUMENT = 'document'
DOCUMENTS = 'documents'
INSERTED_ID = 'insertedId'
INSERTED_IDS = 'insertedIds'
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


tm_event_fields = api.model('TMGetEvents', {
    scraper.TM_POSTAL_CODE: fields.Integer,
    scraper.TM_MAX_PRICE: fields.Integer,
    scraper.TM_START_DATE: fields.DateTime,
    scraper.TM_END_DATE: fields.DateTime,
    scraper.TM_SIZE: fields.Integer
})

sg_event_fields = api.model('SGGetEvents', {
    scraper.SG_POSTAL_CODE: fields.Integer,
    scraper.SG_MAX_PRICE: fields.Integer,
    scraper.SG_START_DATE: fields.DateTime,
    scraper.SG_END_DATE: fields.DateTime,
    scraper.SG_SIZE: fields.Integer
})


mg_tm_fields = api.model('MGTMInsert', {
    scraper.TM_POSTAL_CODE: fields.Integer,
    scraper.TM_MAX_PRICE: fields.Integer,
    scraper.TM_START_DATE: fields.DateTime,
    scraper.TM_END_DATE: fields.DateTime,
    scraper.TM_SIZE: fields.Integer
})


@api.route(f'{TM_GET_EVENTS}')
class TMGetEvents(Resource):
    """
    Simple test to make sure the calls to Ticketmaster's GetEvents
    endpoint is working
    """
    @api.expect(tm_event_fields)
    def post(self):
        '''
        Calls Ticketmaster's API and return a list of events as  POST request
        '''
        postal_code = request.json[scraper.TM_POSTAL_CODE]
        max_price = request.json[scraper.TM_MAX_PRICE]
        # TODO: have a function that process the datetime-local input from the
        # HTML form and converts timezones to UTC
        # At the moment ticketmasterGetEvents assumes this format
        start_date = request.json[scraper.TM_START_DATE]
        end_date = request.json[scraper.TM_END_DATE]
        size = request.json[scraper.TM_SIZE]
        events = scraper.ticketmasterGetEvents(postal_code,
                                               max_price,
                                               start_date,
                                               end_date,
                                               size)
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


@api.route(f'{SG_GET_EVENTS}')
class SGGetEvents(Resource):
    """
    Simple test to make sure the calls to SeatGeek's GetEvents
    endpoint is working
    """
    @api.expect(sg_event_fields)
    def post(self):
        '''
        Calls SeatGeeks's API and return a list of events as  POST request
        '''
        postal_code = request.json[scraper.SG_POSTAL_CODE]
        max_price = request.json[scraper.SG_MAX_PRICE]
        # TODO: have a function that process the datetime-local input from the
        # HTML form and converts timezones to UTC
        start_date = request.json[scraper.SG_START_DATE]
        end_date = request.json[scraper.SG_END_DATE]
        size = request.json[scraper.SG_SIZE]
        events = scraper.seatgeekGetEvents(postal_code, max_price,
                                           start_date, end_date, size)
        return {EVENTS: events}


@api.route(f'{MG_INSERT_DOCUMENT}/<size>/<postalCode>')
class MGInsertDocument(Resource):
    """
    Test to make sure the MongoDB's Atlas Data
    API POST requests can add data
    """
    def post(self, size, postalCode):
        """
        Calls MongoDB's API and inserts a doc, returns inserted ID
        """
        doc = {"size": size, "postalCode": postalCode}
        document = db.POST("insertOne", doc)
        return document


@api.route(f'{MG_TM_INSERT}')
class MGTMInsert(Resource):
    """
    Test insertion of parsed events from Ticketmaster
    into MongoDB collection
    """
    @api.expect(mg_tm_fields)
    def post(self):
        """
        Calls Ticketmaster API and MongoAPI to get events and then
        insert them, returns inserted IDs
        """
        postal_code = request.json[scraper.TM_POSTAL_CODE]
        max_price = request.json[scraper.TM_MAX_PRICE]
        start_date = request.json[scraper.TM_START_DATE]
        end_date = request.json[scraper.TM_END_DATE]
        size = request.json[scraper.TM_SIZE]
        events = scraper.ticketmasterGetEvents(postal_code,
                                               max_price,
                                               start_date,
                                               end_date,
                                               size)
        document = db.POST("insertMany", events)
        return document


@api.route(f'{MG_GET_DOCUMENT}/<size>/<postalCode>')
class MGGetDocument(Resource):
    """
    Test to make sure the MongoDB's Atlas Data
    API POST request can find data
    """
    def post(self, size, postalCode):
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
    def post(self, size, postalCode):
        """
        Calls MongoDB's API and deletes a doc, returning # of items deleted
        """
        doc = {"size": size, "postalCode": postalCode}
        document = db.POST("deleteOne", doc)
        return document


@api.route(f'{MG_GET_MANY}/<size>/<postalCode>')
class MGGetMany(Resource):
    """
    Test to make sure the MongoDB's Atlas Data
    API POST request can find data
    """
    def post(self, size, postalCode):
        """
        Calls MongoDB's API and returns list of documents
        """
        doc = {"size": size, "postalCode": postalCode}
        documents = db.POST("find", doc)
        return documents
