
from sre_constants import ASSERT
import pytest

import server.endpoints as ep
import scraper.scraper as scraper

TEST_CLIENT = ep.app.test_client()

TEST_EVENT_SIZE = 20
TEST_POSTAL_CODE = '10036'
TEST_MAX_PRICE = 200
TEST_START_DATE = "2022-12-01"
TEST_END_DATE = "2022-12-31"


def test_hello():
    """
    See if Hello works.
    """
    resp_json = TEST_CLIENT.get(ep.HELLO).get_json()
    assert isinstance(resp_json[ep.MESSAGE], str)

def test_tm_get_events():
    """
    See if Ticketmaster's GetEvents returns makes a successful POST request and returns
    a list of events (could be empty if no events were found)
    """
    response = TEST_CLIENT.post(f'{ep.TM_GET_EVENTS}', json={
        scraper.POSTAL_CODE: TEST_POSTAL_CODE,
        scraper.MAX_PRICE: TEST_MAX_PRICE,
        scraper.START_DATE: TEST_START_DATE + "T00:00:00Z",
        scraper.END_DATE: TEST_END_DATE + "T23:59:00Z",
        scraper.SIZE: TEST_EVENT_SIZE
    })
    assert response.status_code == 200
    assert isinstance(response.get_json()[ep.EVENTS], list)

def test_sg_get_filtered_events():
    """
    See if Seatgeek's GetFilteredEvents successfully returns a list of filtered events
    (could be empty if no events were found)
    """
    resp_json = TEST_CLIENT.get(f'{ep.SG_FILTERS}/{TEST_MAX_PRICE}/{TEST_POSTAL_CODE}/{TEST_START_DATE}/{TEST_END_DATE}').get_json()
    assert isinstance(resp_json[ep.EVENTS], list)

def test_sg_get_events():
    """
    See if Seatgeek's GetEvents returns makes a successful POST request and returns
    a list of events (could be empty if no events were found)
    """
    response = TEST_CLIENT.post(f'{ep.SG_GET_EVENTS}', json={
        scraper.POSTAL_CODE: TEST_POSTAL_CODE,
        scraper.MAX_PRICE: TEST_MAX_PRICE,
        scraper.START_DATE: TEST_START_DATE + "T00:00:00Z",
        scraper.END_DATE: TEST_END_DATE + "T23:59:00Z",
        scraper.SIZE: TEST_EVENT_SIZE
    })
    assert response.status_code == 200
    assert isinstance(response.get_json()[ep.EVENTS], list)


def test_mg_insert_document():
    """
    See if MongoDB's insertOne returns a string for an inserted event
    """
    resp_json = TEST_CLIENT.post(f'{ep.MG_INSERT_DOCUMENT}/{TEST_EVENT_SIZE}/{TEST_POSTAL_CODE}').get_json()
    assert isinstance(resp_json[ep.INSERTED_ID], str)

def test_mg_get_document():
    """
    See if MongoDB's findOne returns a dictionary of attributes (could be empty if no events were found)
    """
    resp_json = TEST_CLIENT.post(f'{ep.MG_GET_DOCUMENT}/{TEST_EVENT_SIZE}/{TEST_POSTAL_CODE}').get_json()
    assert isinstance(resp_json[ep.DOCUMENT], dict)

def test_mg_delete_document():
    """
    See if MongoDB's deleteOne returns the number of deletedItems (could be zero if no events deleted)
    """
    resp_json = TEST_CLIENT.post(f'{ep.MG_DELETE_DOCUMENT}/{TEST_EVENT_SIZE}/{TEST_POSTAL_CODE}').get_json()
    assert isinstance(resp_json[ep.DELETED_COUNT], int)

def test_mg_get_many():
    """
    See if MongoDB's findMany returns a list of documents (could be empty if no events were found)
    """
    resp_json = TEST_CLIENT.post(f'{ep.MG_GET_MANY}/{TEST_EVENT_SIZE}/{TEST_POSTAL_CODE}').get_json()
    assert isinstance(resp_json[ep.DOCUMENTS], list)

def test_mg_tm_insert():
    """
    See if TM to Mongo insertion results in a list of inserted IDs
    """
    response = TEST_CLIENT.post(f'{ep.MG_TM_INSERT}', json={
        scraper.POSTAL_CODE: TEST_POSTAL_CODE,
        scraper.MAX_PRICE: TEST_MAX_PRICE,
        scraper.START_DATE: TEST_START_DATE + "T00:00:00Z",
        scraper.END_DATE: TEST_END_DATE + "T23:59:00Z",
        scraper.SIZE: TEST_EVENT_SIZE
    })
    assert response.status_code == 200
    assert isinstance(response.get_json()[ep.INSERTED_IDS], list)
