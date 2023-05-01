from sre_constants import ASSERT
import pytest
import server.endpoints as ep
import scraper.scraper as scraper
import scraper.saved_events as s_e

from unittest.mock import patch

TEST_CLIENT = ep.app.test_client()

TEST_PROVIDER = "tm"
TEST_ID = 1231312312
TEST_NAME = "Test Event Name"
TEST_URL = "www.ticketmaster.com/monopoly"
TEST_VENUE_NAME = "Test Venue"
TEST_VENUE_ADDRESS = "12345 Test Avenue"
TEST_DATE = "12 October 20Testing"
TEST_TIME = "10:00:00"
TEST_GENRE = "Rock"
TEST_MIN_PRICE = 10
TEST_EVENT_SIZE = 5
TEST_POSTAL_CODE = '10036'
TEST_MAX_PRICE = 200
TEST_START_DATE = "2023-1-01"
TEST_END_DATE = "2023-1-31"

TEST_EMAIL = "testuser@website.com"
TEST_USERNAME = "test_user"
TEST_PASSWORD = "password123"
TEST_FALSE_USERNAME = "test_ooser"
TEST_FALSE_PASSWORD = "possward123"

TEST_OAUTH_MESSAGE = "Valid OAuth token!"

SAMPLE_EVENT_NM = 'Event1'
SAMPLE_EVENT = {
    s_e.NAME : SAMPLE_EVENT_NM,
    s_e.EVENT_ID: '0', 
}

SAMPLE_PERSON = {
    "name" : TEST_USERNAME,
    "email" : TEST_EMAIL
}


def test_get_events():
    """
    See if Ticketmaster's GetEvents returns makes a successful POST request and returns
    a list of events (could be empty if no events were found)
    """
    response = TEST_CLIENT.post(f'{ep.GET_EVENTS}', json={
        scraper.POSTAL_CODE: TEST_POSTAL_CODE,
        scraper.MAX_PRICE: TEST_MAX_PRICE,
        scraper.START_DATE: TEST_START_DATE + "T00:00:00",
        scraper.END_DATE: TEST_END_DATE + "T23:59:00",
        scraper.SIZE: TEST_EVENT_SIZE
    })

    assert response.status_code == 200
    jsonResp = response.get_json()
    assert isinstance(jsonResp[ep.EVENTS], list)
    assert isinstance(jsonResp[ep.INSERTED_IDS], list)
    events = jsonResp[ep.EVENTS]
    if len(events) > 0:
        assert all('provider' in e for e in events)

def test_add_event():
    """
    test to add event to saved events
    """
    resp = TEST_CLIENT.post(ep.SAVED_ADD, json=SAMPLE_EVENT)
    assert s_e.event_exists(SAMPLE_EVENT_NM)
    s_e.del_event(SAMPLE_EVENT_NM)

@pytest.fixture
def event_size():
    """
    Generates a test event param
    """
    return 5

@pytest.fixture
def postal_code():
    """
    Generates a test event param
    """
    return '10036'

@pytest.mark.skip("token generation not working properly")
def test_oauth_login():
    """
    See if OAuth token is valid, and returns a message corresponding to such.
    """
    resp_json = TEST_CLIENT.get(f'{ep.OAUTH_LOGIN}').get_json()
    assert resp_json[ep.MESSAGE] == TEST_OAUTH_MESSAGE

@pytest.mark.skip("token generation not working properly")
def test_oauth_refresh():
    """
    See if API call can successfully refresh OAuth token
    """
    resp_json = TEST_CLIENT.post(f'{ep.OAUTH_REFRESH_TOKEN}').get_json()
    assert resp_json[ep.RESPONSE] == 200

def test_oauth_set_credentials():
    resp_json = TEST_CLIENT.post(f'{ep.OAUTH_SET_CREDS}').get_json()
    assert resp_json[ep.MESSAGE] == "Credentials successfully set!"

def test_oauth_get_people():
    """
    See if API call can successfully get personal info 
    """
    resp_json = TEST_CLIENT.get(f'{ep.OAUTH_GET_PEOPLE}').get_json()
    assert isinstance(resp_json[ep.RESPONSE], dict)

def test_oauth_and_store():
    """
    See if API call can use personal info to login/register
    """
    resp_json = TEST_CLIENT.get(f'{ep.OAUTH_AND_STORE}').get_json()
    assert resp_json[ep.MESSAGE] == "successful login! or something" or \
                                    "registered with TicketScraper"

def test_oauth_delete_credentials():
    resp_json = TEST_CLIENT.delete(f'{ep.OAUTH_DELETE_CREDS}').get_json()
    assert resp_json[ep.MESSAGE] == "Credentials successfully removed!"

def test_mg_insert_document():
    """
    See if MongoDB's insertOne returns a string for an inserted event
    """
    resp_json = TEST_CLIENT.put(f'{ep.MG_INSERT_DOCUMENT}/{event_size}/{postal_code}').get_json()
    assert isinstance(resp_json[ep.INSERTED_ID], str)

def test_mg_get_document():
    """
    See if MongoDB's findOne returns a dictionary of attributes (could be empty if no events were found)
    """
    resp_json = TEST_CLIENT.get(f'{ep.MG_GET_DOCUMENT}/{event_size}/{postal_code}').get_json()
    assert isinstance(resp_json[ep.DOCUMENT], dict)

def test_mg_delete_document():
    """
    See if MongoDB's deleteOne returns the number of deletedItems (could be zero if no events deleted)
    """
    resp_json = TEST_CLIENT.delete(f'{ep.MG_DELETE_DOCUMENT}/{event_size}/{postal_code}').get_json()
    assert isinstance(resp_json[ep.DELETED_COUNT], int)

def test_mg_get_many():
    """
    See if MongoDB's findMany returns a list of documents (could be empty if no events were found)
    """
    resp_json = TEST_CLIENT.get(f'{ep.MG_GET_MANY}/{TEST_EVENT_SIZE}/{TEST_POSTAL_CODE}').get_json()
    assert isinstance(resp_json[ep.DOCUMENTS], list)

@patch('db.db.people', return_value = SAMPLE_PERSON)
def test_mg_add_favorites(mock_person):
    response = TEST_CLIENT.put(f'{ep.MG_ADD_FAVORITES}', json={
        "provider": TEST_PROVIDER,
        "id": TEST_ID,
        "name": TEST_NAME,
        "url": TEST_URL,
        "venueName": TEST_VENUE_NAME,
        "venueAddress": TEST_VENUE_ADDRESS,
        "eventDate": TEST_DATE,
        "eventTime": TEST_TIME,
        "genre": TEST_GENRE,
        "minPrice": TEST_MIN_PRICE,
        "maxPrice": TEST_MAX_PRICE
    })
    assert response.status_code == 200
    resp_json = response.get_json()
    assert isinstance(resp_json[ep.INSERTED_ID], str)
    """
    See if MGAddFavorites endpoint can save a favorited event
    """

@patch('db.db.people', return_value = SAMPLE_PERSON)
def test_mg_get_favorites(mock_person):
    response = TEST_CLIENT.get(f'{ep.MG_GET_FAVORITES}')
    assert response.status_code == 200
    resp_json = response.get_json()
    assert isinstance(resp_json[ep.DOCUMENTS], list)
    """
    See if MGGetFavorites can get the right favorited event
    """

def test_mg_register():
    """
    See if MongoDB's accounts collection can accept a new, unique account
    """
    resp_json = TEST_CLIENT.post(f'{ep.MG_REGISTER}'
                                 f'/{TEST_EMAIL}'
                                 f'/{TEST_USERNAME}'
                                 f'/{TEST_PASSWORD}').get_json()
    assert isinstance(resp_json[ep.INSERTED_ID], str)

def test_login():
    """
    See if MongoDB can check if login credentials are accurate
    """
    resp_json = TEST_CLIENT.put(f'{ep.MG_LOGIN}'
                                 f'/{TEST_USERNAME}'
                                 f'/{TEST_PASSWORD}').get_json()
    assert resp_json[ep.RESPONSE] == True

def test_login_fail():
    """
    See if the login endpoint can properly reject incorrect attempts
    """
    resp_1 = TEST_CLIENT.put(f'{ep.MG_LOGIN}'
                                 f'/{TEST_FALSE_USERNAME}'
                                 f'/{TEST_PASSWORD}').get_json()
    assert resp_1[ep.MESSAGE] == "No account with that username found"
    resp_2 = TEST_CLIENT.put(f'{ep.MG_LOGIN}'
                                 f'/{TEST_USERNAME}'
                                 f'/{TEST_FALSE_PASSWORD}').get_json()
    assert resp_2[ep.MESSAGE] == "Incorrect password."

def test_all_insert():
    """
    See if TM and SG to Mongo insertion results in two lists of inserted IDs
    (this basically checks if all three API keys are working properly)
    """
    response = TEST_CLIENT.put(f'{ep.ALL_INSERT}', json={
        scraper.POSTAL_CODE: TEST_POSTAL_CODE,
        scraper.MAX_PRICE: TEST_MAX_PRICE,
        scraper.START_DATE: TEST_START_DATE + "T00:00:00Z",
        scraper.END_DATE: TEST_END_DATE + "T23:59:00Z",
        scraper.SIZE: TEST_EVENT_SIZE
    })
    assert response.status_code == 200
    resp_json = response.get_json()
    #check response
    assert isinstance(resp_json[ep.INSERTED_IDS], list)

def test_get_and_convert():
    """
    See if the get_and_convert endpoint returns a list of Events(could be empty if no events were found)
    """
    response = TEST_CLIENT.get(f'{ep.GET_AND_CONVERT}', json={
        scraper.MAX_PRICE: TEST_MAX_PRICE,
        scraper.START_DATE: TEST_START_DATE + "T00:00:00Z",
    })
    assert response.status_code == 200
    resp_json = response.get_json()
    assert isinstance(resp_json[ep.EVENTS], list)
    if len(resp_json[ep.EVENTS]) > 0:
        assert isinstance(resp_json[ep.EVENTS][0], scraper.Event)

#@pytest.mark.skip(reason = "Don't want to clear entire DB just yet")
def test_all_clear():
    resp_json = TEST_CLIENT.delete(f'{ep.ALL_CLEAR}').get_json()
    assert isinstance(resp_json[ep.DELETED_COUNT], int)

def test_all_genres():
    """
    Test if a list of all the genres is returned from scraper.py
    """
    response = TEST_CLIENT.get('/AllGenres')
    assert response.status_code == 200
    resp_json = response.get_json()
    assert isinstance(resp_json["genres"], list)

