
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
        scraper.START_DATE: TEST_START_DATE + "T00:00:00",
        scraper.END_DATE: TEST_END_DATE + "T23:59:00",
        scraper.SIZE: TEST_EVENT_SIZE
    })
    assert response.status_code == 200
    assert isinstance(response.get_json()[ep.EVENTS], list)


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

def test_all_insert():
    """
    See if TM and SG to Mongo insertion results in two lists of inserted IDs
    (this basically checks if all three API keys are working properly)
    """
    response = TEST_CLIENT.post(f'{ep.ALL_INSERT}', json={
        scraper.POSTAL_CODE: TEST_POSTAL_CODE,
        scraper.MAX_PRICE: TEST_MAX_PRICE,
        scraper.START_DATE: TEST_START_DATE + "T00:00:00Z",
        scraper.END_DATE: TEST_END_DATE + "T23:59:00Z",
        scraper.SIZE: TEST_EVENT_SIZE
    })
    assert response.status_code == 200
    resp_json = response.get_json()
    #check TM response
    assert isinstance(resp_json[ep.TM][ep.INSERTED_IDS], list)
    #check SG response
    assert isinstance(resp_json[ep.SG][ep.INSERTED_IDS], list)

def test_get_and_convert():
    """
    See if the get_and_convert endpoint returns a list of Events(could be empty if no events were found)
    """
    resp_json = TEST_CLIENT.post(f'{ep.GET_AND_CONVERT}/{TEST_EVENT_SIZE}').get_json()
    assert isinstance(resp_json[ep.EVENTS], list)
    if len(resp_json[ep.EVENTS]) > 0:
        assert isinstance(resp_json[ep.EVENTS][0], scraper.Event)