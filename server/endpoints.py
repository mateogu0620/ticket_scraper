"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask
from flask_restx import Resource, Api
from pymongo import MongoClient
from scraper import scraper

app = Flask(__name__)
api = Api(app)

client = MongoClient('localhost', 27017)
# Username: Cluster08493
# Password: RlhRbmFKSH1E
db = client.flask_db  # creating mongoDB instance
collection = db.collec

LIST = 'list'
HELLO = '/hello'
MESSAGE = 'message'
TM_GET_EVENTS = '/tm_get_events'
SG_GET_EVENTS = '/sg_get_events'
EVENTS = 'events'


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


@api.route(f'{TM_GET_EVENTS}/<size>/<postalCode>')
class TMGetEvents(Resource):
    """
    Simple test to make sure the calls to Ticketmaster's GetEvents
    endpoint is working
    """
    def get(self, size, postalCode):
        """
        Calls Ticketmaster's API and return a list of events
        """
        events = scraper.ticketmasterGetEvents(size, postalCode)
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
