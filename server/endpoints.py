"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
import sys
import os
import json
import copy
from flask import Flask, request
from flask_restx import Resource, Api, fields, Namespace
from flask_cors import CORS
from scraper import scraper
from scraper import saved_events as se
from scraper import share
from scraper import URL
from db import db

print(sys.path)

app = Flask(__name__)
CORS(app)
api = Api(app)

SAVED_NS = 'events'
SHARE_NS = 'sites'
URL_NS = 'url'

events_ns = Namespace(SAVED_NS, 'Saved_Events')
api.add_namespace(events_ns)
sites_ns = Namespace(SHARE_NS, 'SM_Sites')
api.add_namespace(sites_ns)

LIST = 'list'
DICT = 'dict'
MESSAGE = 'message'
TM = "TICKETMASTER"
SG = "SEATGEEK"
TM_GET_EVENTS = '/tm_get_events'
SG_GET_EVENTS = '/sg_get_events'
OAUTH_SET_CREDS = '/oauth_set_credentials'
OAUTH_DELETE_CREDS = '/oauth_delete_credentials'
OAUTH_REFRESH_TOKEN = '/oauth_refresh_token'
OAUTH_GET_PEOPLE = '/oauth_get_people'
OAUTH_LOGIN = '/oauth_login'
OAUTH_AND_STORE = '/oauth_and_store'
GET_EVENTS = '/get-events'
MG_GET_DOCUMENT = '/mg_get_document'
MG_INSERT_DOCUMENT = '/mg_insert_document'
MG_DELETE_DOCUMENT = '/mg_delete_document'
MG_GET_MANY = '/mg_get_many'
ALL_INSERT = '/all_insert'
ALL_CLEAR = '/all_clear'
GET_AND_CONVERT = '/get_and_convert'
MG_REGISTER = '/mg_register'
MG_LOGIN = '/mg_login'
MG_ADD_FAVORITES = '/mg_add_favorites'
MG_GET_FAVORITES = '/mg_get_favorites'
DELETE_ACCOUNT = '/delete_account'
FILTER = 'filter'
EVENTS = 'events'
DOCUMENT = 'document'
DOCUMENTS = 'documents'
INSERTED_ID = 'insertedId'
INSERTED_IDS = 'insertedIds'
DELETED_COUNT = 'deletedCount'
PROFILE_MENU = '/profile_menu'
PROFILE_MENU_NM = 'Profile Menu'
SHARE_TYPES_NS = 'share_types'

TEST_EVENT = 'test_event'
RESPONSE = 'response'

SAVED_DICT = f'/{DICT}'
SAVED_DICT_W_NS = f'{SAVED_NS}/{DICT}'
SAVED_ADD = f'/{SAVED_NS}/add'
SHARE_DICT = f'/{DICT}'
SHARE_DICT_W_NS = f'{SHARE_NS}/{DICT}'
SHARE_DICT_NM = f'{SHARE_NS}_dict'
URL_DICT = f'/{DICT}'
URL_DICT_W_NS = f'{URL_NS}/{DICT}'
URL_ADD = f'/{URL_NS}/add'


tm_event_fields = api.model('TMGetEvents', {
    scraper.POSTAL_CODE: fields.Integer,
    scraper.MAX_PRICE: fields.Integer,
    scraper.START_DATE: fields.DateTime,
    scraper.END_DATE: fields.DateTime,
    scraper.SIZE: fields.Integer,
    scraper.GENRE: fields.String
})

sg_event_fields = api.model('SGGetEvents', {
    scraper.POSTAL_CODE: fields.Integer,
    scraper.MAX_PRICE: fields.Integer,
    scraper.START_DATE: fields.DateTime,
    scraper.END_DATE: fields.DateTime,
    scraper.SIZE: fields.Integer,
    scraper.GENRE: fields.String
})

all_fields = api.model('AllInsert', {
    scraper.POSTAL_CODE: fields.Integer,
    scraper.MAX_PRICE: fields.Integer,
    scraper.START_DATE: fields.DateTime,
    scraper.END_DATE: fields.DateTime,
    scraper.SIZE: fields.Integer,
    scraper.GENRE: fields.String
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
    scraper.SIZE: fields.Integer,
    scraper.GENRE: fields.String
})

mg_favorite_event_fields = api.model('MGAddFavorites', {
    "provider": fields.String,
    "id": fields.Integer,
    "name": fields.String,
    "url": fields.String,
    "venueName": fields.String,
    "venueAddress": fields.String,
    "eventDate": fields.String,
    "eventTime": fields.String,
    "genre": fields.String,
    "minPrice": fields.Integer,
    "maxPrice": fields.Integer
})

save_event_fields = api.model('NewEvent', {
    se.NAME: fields.String,
    se.EVENT_ID: fields.String,
})

save_event_fields = api.model('NewEvent', {
    se.NAME: fields.String,
    se.EVENT_ID: fields.String,
})

save_usernames = api.model('setUserName', {
    se.NAME: fields.String,
})

save_password = api.model('setPassword', {
    se.NAME: fields.String,
})

save_zipcode_preference = api.model('setSserZipCode', {
    se.NAME: fields.String,
})


@api.route(f'{GET_EVENTS}')
class GetEvents(Resource):
    """
    Making API calls to Ticketmaster and Seatgeek and return a list of events
    matching the user-provided filters
    """
    @api.expect(generic_event_fields)
    def post(self):
        """
        Making API calls to Ticketmaster and Seatgeek and return a list of
        events matching the user-provided filters.
        """
        postal_code = request.json[scraper.POSTAL_CODE]
        max_price = request.json[scraper.MAX_PRICE]
        start_date = request.json[scraper.START_DATE]
        end_date = request.json[scraper.END_DATE]
        size = int(request.json[scraper.SIZE])
        if scraper.GENRE in request.json:
            genre = request.json[scraper.GENRE]
        else:
            genre = None
        print(postal_code, max_price, start_date, end_date, size, genre)
        events = scraper.getEvents(postal_code,
                                   max_price,
                                   start_date,
                                   end_date,
                                   size,
                                   genre)
        jsonEvents = [e.toDict() for e in events]
        jsonEventsDB = copy.deepcopy(jsonEvents)

        response = db.POST("insertMany", "events", jsonEventsDB)

        return {EVENTS: jsonEvents, INSERTED_IDS: response[INSERTED_IDS]}


@api.route(f'{OAUTH_LOGIN}')
class OAuthLogin(Resource):
    """
    Generate OAuth token by logging in
    """
    def get(self):
        """
        Calls OAuth token checker function, returns message
        for success or new token required
        """
        response = db.login()
        return response


@api.route(f'{OAUTH_AND_STORE}')
class OAuthAndStore(Resource):
    """
    Get info and login/register.
    """
    def put(self):
        """
        Call authentication and storage method, register or login.
        """
        message = db.authenticate_and_store()
        return {MESSAGE: message}


@api.route(f'{OAUTH_SET_CREDS}')
class OAuthSetCredentials(Resource):
    """
    Endpoint for setting OAuth credentials
    """
    def post(self):
        """
        Calls OAuth set credential function, gets credentials
        """
        response = db.set_credentials()
        try:
            f = open("credentials.json", "x")
            json.dump(response, f)
        except OSError:
            return {MESSAGE: "OSError: file already exists"}
        finally:
            return {MESSAGE: "Credentials successfully set!"}


@api.route(f'{MG_ADD_FAVORITES}')
class MGAddFavorites(Resource):
    """
    Endpoint for adding a favorite event
    """
    @api.expect(mg_favorite_event_fields)
    def put(self):
        """
        Calls MongoDB insertOne function, puts in a favorite event
        """
        event = {
            "provider": request.json["provider"],
            "id": request.json["id"],
            "name": request.json["name"],
            "url": request.json["url"],
            "venueName": request.json["venueName"],
            "eventDate": request.json["eventDate"],
            "eventTime": request.json["eventTime"],
            "genre": request.json["genre"],
            "minPrice": request.json["minPrice"],
            "maxPrice": request.json["maxPrice"],
        }
        login = db.people()
        event["name"] = login["name"]
        event["email"] = login["email"]
        response = db.POST("insertOne", "favorites", event)
        return response


@api.route(f'{MG_GET_FAVORITES}')
class MGGetFavorites(Resource):
    """
    Endpoint for getting favorite events
    """
    def get(self):
        """
        Calls MongoDB findMany function, gets list of events
        """
        login = db.people()
        response = db.POST("find", "favorites", login)
        return response


@api.route(f'{OAUTH_DELETE_CREDS}')
class OAuthDeleteCredentials(Resource):
    """
    Endpoint for removing OAuth credentials
    """
    def delete(self):
        """
        Removes creds
        """
        try:
            os.remove("credentials.json")
        except FileNotFoundError:
            return {MESSAGE: "FileNotFoundError: no file to delete"}
        return {MESSAGE: "Credentials successfully removed!"}


@api.route(f'{OAUTH_REFRESH_TOKEN}')
class OAuthRefreshToken(Resource):
    """
    Endpoint for refreshing OAuth token
    """
    def post(self):
        """
        Refreshes token
        """
        response = db.refresh_token()
        return {RESPONSE: response}


@api.route(f'{OAUTH_GET_PEOPLE}')
class OAuthGetPeople(Resource):
    """
    Endpoint for getting information from user
    """
    def get(self):
        response = db.people()
        return {RESPONSE: response}


@api.route(f'{MG_INSERT_DOCUMENT}/<size>/<postalCode>')
class MGInsertDocument(Resource):
    """
    Test to make sure the MongoDB's Atlas Data
    API POST requests can add data
    """
    def put(self, size, postalCode):
        """
        Calls MongoDB's API and inserts a doc, returns inserted ID
        """
        doc = {"size": size, "postalCode": postalCode}
        document = db.POST("insertOne", "events", doc)
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
        filter = {"size": size, "postalCode": postalCode}
        document = db.POST("findOne", "events", filter)
        return document


@api.route(f'{MG_DELETE_DOCUMENT}/<size>/<postalCode>')
class MGDeleteDocument(Resource):
    """
    Test to make sure the MongoDB's Atlas Data
    API POST request can find data
    """
    def delete(self, size, postalCode):
        """
        Calls MongoDB's API and deletes a doc, returning # of items deleted
        """
        doc = {"size": size, "postalCode": postalCode}
        document = db.POST("deleteOne", "events", doc)
        return document


@api.route(f'{MG_GET_MANY}/<size>/<postalCode>')
class MGGetMany(Resource):
    """
    Test to make sure the MongoDB's Atlas Data
    API POST request can find data
    """
    def get(self, size, postalCode):
        """
        Calls MongoDB's API and returns list of documents
        """
        doc = {"size": size, "postalCode": postalCode}
        documents = db.POST("find", "events", doc)
        return documents


@api.route(f'{MG_REGISTER}/<email>/<username>/<password>')
class MGRegister(Resource):
    """
    Test registration with MongoDB
    """
    def post(self, email, username, password):
        """
        Call POST method to check duplicates, then register
        """
        doc = {
            "email": email,
            "username": username,
            "password": password
        }
        if len(db.POST("find",
                       "accounts",
                       {"email": email})
               [DOCUMENTS]) > 0:
            raise Exception("An account with this email already exists")
        elif len(db.POST("find",
                         "accounts",
                         {"username": username})
                 [DOCUMENTS]) > 0:
            raise Exception("An account with this username already exists")
        response = db.POST("insertOne", "accounts", doc)
        return response


@api.route(f'{MG_LOGIN}/<username>/<password>')
class MGLogin(Resource):
    """
    Test login with MongoDB
    """
    def put(self, username, password):
        """
        Call POST method to check if password is correct
        """
        doc = db.POST("findOne",
                      "accounts",
                      {"username": username})
        if doc[DOCUMENT] is None:
            return {MESSAGE: "No account with that username found"}
        elif not (doc[DOCUMENT]["password"] == password):
            return {MESSAGE: "Incorrect password."}
        else:
            return {RESPONSE: True}


@api.route(f'{ALL_CLEAR}')
class AllClear(Resource):
    """
    Clears the entire MongoDB account collection
    """
    def delete(self):
        """
        Calls MongoDB's API and returns number of deleted documents
        """
        document = db.POST("deleteMany", "accounts", {})
        return document


@api.route(f'{GET_AND_CONVERT}')
class GetAndConvert(Resource):
    """
    MongoDB data API returning list of dicts and converting them
    to Event objects
    """
    @api.expect(get_fields)
    def get(self):
        """
        Calls MongoDB's API and returns documents to be converted
        """
        max_price = request.json[scraper.MAX_PRICE]
        start_date = request.json[scraper.START_DATE]
        filter = {
            "maxPrice": max_price,
            "eventDate": start_date
        }
        documents = db.POST("find", "events", filter)
        events = db.convertToEvent(documents[DOCUMENTS])
        return {EVENTS: events}


@api.route(f'{DELETE_ACCOUNT}')
class DeleteAccount(Resource):
    """
    API for removing all traces of an account from the database.
    """
    def put(self):
        doc = db.people()
        result1 = db.POST("deleteMany", "favorites", doc)
        result2 = db.POST("deleteOne", "accounts", doc)
        return {
            "favorites": result1,
            "accounts": result2
            }


@api.route(PROFILE_MENU)
class ProfileBar(Resource):
    """
    Will deliver the drop down task bar
    """
    def get(self):
        """
        Gets the drop down task bar
        """
        return {'Title': PROFILE_MENU_NM,
                'Default': 0,
                'Choices': {
                    '1': {'url': f'/{URL_DICT_W_NS}',
                          'method': 'get', 'text': 'My Profile'},
                    '2': {'url': f'/{URL_DICT_W_NS}',
                          'method': 'get', 'text': 'Settings'},
                    '3': {'url': f'/{URL_DICT_W_NS}',
                          'method': 'get', 'text': 'Log In'},
                    'X': {'text': 'Exit'},
                }}


@api.route(URL_DICT)
class UrlDict(Resource):
    """
    This will get a list of currrent saved events.
    """
    def get(self):
        """
        Returns a list of current events user has saved.
        """
        return {'Data': URL.get_url(),
                'Type': 'Data',
                'Title': 'Saved Events'}


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
    Add a Event to saved events.
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


@api.route(f'/{TEST_EVENT}react')
class ReactTest(Resource):
    def getEventsREACT():
        return {"events": ["Event1", "Event2"]}


@api.route('/AllGenres')
class AllGenres(Resource):
    def get(self):
        """
        Returns a list of all genres used in both APIs
        """
        in_both = scraper.GENRES_INBOTH
        tm_only = scraper.GENRES_TMONLY
        all_genres = in_both + tm_only
        return {"genres": sorted(all_genres)}
