from sre_constants import ASSERT
import pytest
import server.endpoints as ep
import scraper.scraper as scraper
import scraper.saved_events as s_e

TEST_CLIENT = ep.app.test_client()

TEST_EVENT_SIZE = 5
TEST_POSTAL_CODE = '10036'
TEST_MAX_PRICE = 200
TEST_START_DATE = "2023-1-01"
TEST_END_DATE = "2023-1-31"

TEST_EMAIL = "testuser@website.com"
TEST_USERNAME = "test_user"
TEST_PASSWORD = "password123"

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
        scraper.START_DATE: TEST_START_DATE + "T00:00:00",
        scraper.END_DATE: TEST_END_DATE + "T23:59:00",
        scraper.SIZE: TEST_EVENT_SIZE
    })
    assert response.status_code == 200
    assert isinstance(response.get_json()[ep.EVENTS], list)

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
    # TODO: some check here to make sure these events are in the correct GenericEvent format. Using this for now
    events = jsonResp[ep.EVENTS]
    if len(events) > 0:
        assert all('provider' in e for e in events)

def test_mg_insert_document():
    """
    See if MongoDB's insertOne returns a string for an inserted event
    """
    resp_json = TEST_CLIENT.post(f'{ep.MG_INSERT_DOCUMENT}/{event_size}/{postal_code}').get_json()
    assert isinstance(resp_json[ep.INSERTED_ID], str)

def test_mg_get_document():
    """
    See if MongoDB's findOne returns a dictionary of attributes (could be empty if no events were found)
    """
    resp_json = TEST_CLIENT.post(f'{ep.MG_GET_DOCUMENT}/{event_size}/{postal_code}').get_json()
    assert isinstance(resp_json[ep.DOCUMENT], dict)

def test_mg_delete_document():
    """
    See if MongoDB's deleteOne returns the number of deletedItems (could be zero if no events deleted)
    """
    resp_json = TEST_CLIENT.post(f'{ep.MG_DELETE_DOCUMENT}/{event_size}/{postal_code}').get_json()
    assert isinstance(resp_json[ep.DELETED_COUNT], int)

def test_mg_get_many():
    """
    See if MongoDB's findMany returns a list of documents (could be empty if no events were found)
    """
    resp_json = TEST_CLIENT.post(f'{ep.MG_GET_MANY}/{TEST_EVENT_SIZE}/{TEST_POSTAL_CODE}').get_json()
    assert isinstance(resp_json[ep.DOCUMENTS], list)

def test_mg_register():
    """
    See if MongoDB's accounts collection can accept a new, unique account
    """
    resp_json = TEST_CLIENT.post(f'{ep.MG_REGISTER}'
                                 f'/{TEST_EMAIL}'
                                 f'/{TEST_USERNAME}'
                                 f'/{TEST_PASSWORD}').get_json()
    assert isinstance(resp_json[ep.INSERTED_ID], str)

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
    #check response
    assert isinstance(resp_json[ep.INSERTED_IDS], list)

def test_get_and_convert():
    """
    See if the get_and_convert endpoint returns a list of Events(could be empty if no events were found)
    """
    response = TEST_CLIENT.post(f'{ep.GET_AND_CONVERT}', json={
        scraper.MAX_PRICE: TEST_MAX_PRICE,
        scraper.START_DATE: TEST_START_DATE + "T00:00:00Z",
    })
    assert response.status_code == 200
    resp_json = response.get_json()
    assert isinstance(resp_json[ep.EVENTS], list)
    if len(resp_json[ep.EVENTS]) > 0:
        assert isinstance(resp_json[ep.EVENTS][0], scraper.Event)

SAMPLE_EVENT_NM = 'Event1'
SAMPLE_EVENT = {
    s_e.NAME : SAMPLE_EVENT_NM,
    s_e.EVENT_ID: '0', 
}

def test_add_event():
    """
    test to add event to saved events
    """
    resp = TEST_CLIENT.post(ep.SAVED_ADD, json=SAMPLE_EVENT)
    assert s_e.event_exists(SAMPLE_EVENT_NM)
    s_e.del_event(SAMPLE_EVENT_NM)

#@pytest.mark.skip(reason = "Don't want to clear entire DB just yet")
def test_all_clear():
    resp_json = TEST_CLIENT.post(f'{ep.ALL_CLEAR}').get_json()
    assert isinstance(resp_json[ep.DELETED_COUNT], int)

