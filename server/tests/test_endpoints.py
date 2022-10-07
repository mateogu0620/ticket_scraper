
import pytest

import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()

TEST_EVENT_SIZE = 1
TEST_POSTAL_CODE = '10036'
TEST_DOC_FIRSTNAME = "Alan"
TEST_DOC_LASTNAME = "Turing"


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

def test_mg_get_document():
    """
    See if MongoDB's findOne returns a dictionary of attributes (could be empty if no events were found)
    """
    resp_json = TEST_CLIENT.get(f'{ep.MG_GET_DOCUMENT}/{TEST_DOC_FIRSTNAME}/{TEST_DOC_LASTNAME}').get_json()
    assert isinstance(resp_json[ep.DOCUMENT], dict)