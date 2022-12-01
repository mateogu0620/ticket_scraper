"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask, request
from flask_restx import Resource, Api, fields, Namespace
from scraper import scraper
from scraper import saved_events as se
from scraper import share
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

SAVED_NS = 'events'
SHARE_NS = 'sites'

events_ns = Namespace(SAVED_NS, 'Saved_Events')
api.add_namespace(events_ns)
sites_ns = Namespace(SHARE_NS, 'SM_Sites')
api.add_namespace(sites_ns)

LIST = 'list'
DICT = 'dict'
HELLO = '/hello'
MESSAGE = 'message'
TM = "TICKETMASTER"
SG = "SEATGEEK"
TM_GET_EVENTS = '/tm_get_events'
SG_GET_EVENTS = '/sg_get_events'
GET_EVENTS = '/get-events'
MG_GET_DOCUMENT = '/mg_get_document'
MG_INSERT_DOCUMENT = '/mg_insert_document'
MG_DELETE_DOCUMENT = '/mg_delete_document'
MG_GET_MANY = '/mg_get_many'
ALL_INSERT = '/all_insert'
ALL_CLEAR = '/all_clear'
GET_AND_CONVERT = '/get_and_convert'
FILTER = 'filter'
EVENTS = 'events'
DOCUMENT = 'document'
DOCUMENTS = 'documents'
INSERTED_ID = 'insertedId'
INSERTED_IDS = 'insertedIds'
DELETED_COUNT = 'deletedCount'
EVENT_MENU = '/event_menu'
EVENT_MENU_NM = 'Event Menu'
SHARE_TYPES_NS = 'share_types'
TEST_EVENT = 'test_event'

SAVED_DICT = f'/{DICT}'
SAVED_DICT_W_NS = f'{SAVED_NS}/{DICT}'
SAVED_ADD = f'/{SAVED_NS}/add'

SHARE_DICT = f'/{DICT}'
SHARE_DICT_W_NS = f'{SHARE_NS}/{DICT}'
SHARE_DICT_NM = f'{SHARE_NS}_dict'


tm_event_fields = api.model('TMGetEvents', {
    scraper.POSTAL_CODE: fields.Integer,
    scraper.MAX_PRICE: fields.Integer,
    scraper.START_DATE: fields.DateTime,
    scraper.END_DATE: fields.DateTime,
    scraper.SIZE: fields.Integer
})

sg_event_fields = api.model('SGGetEvents', {
    scraper.POSTAL_CODE: fields.Integer,
    scraper.MAX_PRICE: fields.Integer,
    scraper.START_DATE: fields.DateTime,
    scraper.END_DATE: fields.DateTime,
    scraper.SIZE: fields.Integer
})

all_fields = api.model('AllInsert', {
    scraper.POSTAL_CODE: fields.Integer,
    scraper.MAX_PRICE: fields.Integer,
    scraper.START_DATE: fields.DateTime,
    scraper.END_DATE: fields.DateTime,
    scraper.SIZE: fields.Integer
})

get_fields = api.model('GetAndConvert', {
    scraper.MAX_PRICE: fields.Integer,
    scraper.START_DATE: fields.DateTime,
})

generic_event_fields = api.model('GetEvents', {
    scraper.POSTAL_CODE: fields.Integer,
    scraper.MAX_PRICE: fields.Integer,
    scraper.START_DATE: fields.DateTime,
    scraper.END_DATE: fields.DateTime,
    scraper.SIZE: fields.Integer
})

save_event_fields = api.model('NewEvent', {
    se.NAME: fields.String,
    se.EVENT_ID: fields.String,
})


@api.route(f'{TM_GET_EVENTS}')
class TMGetEvents(Resource):
    """
    Making an API call to Ticketmaster and returning the list of events
    matching the user-provided filters
    """
    @api.expect(tm_event_fields)
    def post(self):
        '''
        Calls Ticketmaster's API and return a list of events as POST request
        '''
        postal_code = request.json[scraper.POSTAL_CODE]
        max_price = request.json[scraper.MAX_PRICE]
        start_date = request.json[scraper.START_DATE]
        end_date = request.json[scraper.END_DATE]
        size = request.json[scraper.SIZE]
        # Return a list of TMEvents
        events = scraper.ticketmasterGetEvents(postal_code,
                                               max_price,
                                               start_date,
                                               end_date,
                                               size)
        jsonEvents = [e.toDict() for e in events]
        return {EVENTS: jsonEvents}


@api.route(f'{SG_GET_EVENTS}')
class SGGetEvents(Resource):
    """
    Making an API call to SeatGeek and returning the list of events
    matching the user-provided filters
    """
    @api.expect(sg_event_fields)
    def post(self):
        '''
        Calls SeatGeeks's API and return a list of events as POST request
        '''
        postal_code = request.json[scraper.POSTAL_CODE]
        max_price = request.json[scraper.MAX_PRICE]
        # TODO: have a function that process the datetime-local input from the
        # HTML form and converts timezones to UTC
        start_date = request.json[scraper.START_DATE]
        end_date = request.json[scraper.END_DATE]
        size = request.json[scraper.SIZE]
        events = scraper.seatgeekGetEvents(postal_code, max_price,
                                           start_date, end_date, size)
        events = [e.toDict() for e in events]
        return {EVENTS: events}


@api.route(f'{GET_EVENTS}')
class GetEvents(Resource):
    """
    Making API calls to Ticketmaster and Seatgeek and return a list of events
    matching the user-provided filters
    """
    @api.expect(generic_event_fields)
    def post(self):
        postal_code = request.json[scraper.POSTAL_CODE]
        max_price = request.json[scraper.MAX_PRICE]
        start_date = request.json[scraper.START_DATE]
        end_date = request.json[scraper.END_DATE]
        size = request.json[scraper.SIZE]
        events = scraper.getEvents(postal_code,
                                   max_price,
                                   start_date,
                                   end_date,
                                   size)
        jsonEvents = [e.toDict() for e in events]
        return {EVENTS: jsonEvents}


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
        filter = {"size": size, "postalCode": postalCode}
        document = db.POST("findOne", filter)
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


@api.route(f'{ALL_INSERT}')
class AllInsert(Resource):
    """
    Test insertion of parsed events from Ticketmaster and Seatgeek
    into MongoDB collection
    """
    @api.expect(all_fields)
    def post(self):
        """
        Calls Ticketmaster, SeatGeek, and MongoAPI to get events and then
        insert them, returns inserted IDs for both
        """
        postal_code = request.json[scraper.POSTAL_CODE]
        max_price = request.json[scraper.MAX_PRICE]
        start_date = request.json[scraper.START_DATE]
        end_date = request.json[scraper.END_DATE]
        size = request.json[scraper.SIZE]
        events = scraper.getEvents(postal_code,
                                   max_price,
                                   start_date,
                                   end_date,
                                   size)

        for i in range(len(events)):
            events[i] = events[i].toDict()

        response = db.POST("insertMany", events)
        return response


@api.route(f'{ALL_CLEAR}')
class AllClear(Resource):
    """
    Clears the entire MongoDB Event collection
    """
    def post(self):
        """
        Calls MongoDB's API and returns number of deleted documents
        """
        document = db.POST("deleteMany", {})
        return document


@api.route(f'{GET_AND_CONVERT}')
class GetAndConvert(Resource):
    """
    MongoDB data API returning list of dicts and converting them
    to Event objects
    """
    @api.expect(get_fields)
    def post(self):
        """
        Calls MongoDB's API and returns documents to be converted
        """
        max_price = request.json[scraper.MAX_PRICE]
        start_date = request.json[scraper.START_DATE]
        filter = {
            "maxPrice": max_price,
            "eventDate": start_date
        }
        documents = db.POST("find", filter)
        events = db.convertToEvent(documents[DOCUMENTS])
        return {EVENTS: events}


@api.route(EVENT_MENU)
class MainMenu(Resource):
    """
    This will deliver our main menu.
    """
    def get(self):
        """
        Gets the main game menu.
        """
        return {'Title': EVENT_MENU_NM,
                'Default': 0,
                'Choices': {
                    '1': {'url': f'/{SAVED_DICT_W_NS}',
                          'method': 'get', 'text': 'Save Event'},
                    '2': {'url': f'/{SHARE_DICT_W_NS}',
                          'method': 'get', 'text': 'List where to share'},
                    'X': {'text': 'Exit'},
                }}


@api.route(SAVED_DICT)
class SavedDict(Resource):
    """
    This will get a list of currrent saved events.
    """
    def get(self):
        """
        Returns a list of current events user has saved.
        """
        return {'Data': se.get_events_dict(),
                'Type': 'Data',
                'Title': 'Saved Events'}


@api.route(SHARE_DICT)
class SitesDict(Resource):
    """
    This will get a list of currrent websites to share events.
    """
    def get(self):
        """
        Returns a list of current saved websites to share with.
        """
        return {'Data': share.get_sites_dict(),
                'Type': 'Data',
                'Title': 'Saved Websites'}


@api.route(SAVED_ADD)
class AddEvent(Resource):
    """
    Add a Event.
    """
    @api.expect(save_event_fields)
    def post(self):
        """
        Add a Event.
        """
        print(f'{request.json=}')
        name = request.json[se.NAME]
        del request.json[se.NAME]
        se.add_event(name, request.json)
