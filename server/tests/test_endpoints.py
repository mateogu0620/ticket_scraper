
import pytest

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()

TEST_EVENT_SIZE = 1
TEST_POSTAL_CODE = '10036'


def test_hello():
    """
    See if Hello works.
    """
    resp_json = TEST_CLIENT.get(ep.HELLO).get_json()
    assert isinstance(resp_json[ep.MESSAGE], str)

def test_tm_get_events():
    """
    See if Ticketmaster's GetEvents return a list of events (could be empty if no events were found)
    """
    resp_json = TEST_CLIENT.get(f'{ep.TM_GET_EVENTS}/{TEST_EVENT_SIZE}/{TEST_POSTAL_CODE}').get_json()
    assert isinstance(resp_json[ep.EVENTS], list)

def test_sg_get_events():
    """
    See if Seatgeek's GetEvents returns a list of events (could be empty if no events were found)
    """
    resp_json = TEST_CLIENT.get(f'{ep.SG_GET_EVENTS}/{TEST_EVENT_SIZE}/{TEST_POSTAL_CODE}').get_json()
    assert isinstance(resp_json[ep.EVENTS], list)

def test_mg_insert_document():
    """
    See if MongoDB's insertOne returns a string for an inserted event
    """
    resp_json = TEST_CLIENT.get(f'{ep.MG_INSERT_DOCUMENT}/{TEST_EVENT_SIZE}/{TEST_POSTAL_CODE}').get_json()
    assert isinstance(resp_json[ep.INSERTED_ID], str)

def test_mg_get_document():
    """
    See if MongoDB's findOne returns a dictionary of attributes (could be empty if no events were found)
    """
    resp_json = TEST_CLIENT.get(f'{ep.MG_GET_DOCUMENT}/{TEST_EVENT_SIZE}/{TEST_POSTAL_CODE}').get_json()
    assert isinstance(resp_json[ep.DOCUMENT], dict)

def test_mg_delete_document():
    """
    See if MongoDB's deleteOne returns the number of deletedItems (could be zero if no events deleted)
    """
    resp_json = TEST_CLIENT.get(f'{ep.MG_DELETE_DOCUMENT}/{TEST_EVENT_SIZE}/{TEST_POSTAL_CODE}').get_json()
    assert isinstance(resp_json[ep.DELETED_COUNT], int)