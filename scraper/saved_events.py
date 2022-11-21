TEST_EVENT_NAME = 'Test event'
NAME = 'name'
EVENT_ID = 'id'

REQUIRED_FLDS = [EVENT_ID]
events = {TEST_EVENT_NAME: {EVENT_ID: 0},
         'event1': {EVENT_ID: 1},
         'event2': {EVENT_ID: 1}, }


def event_exists(name):
    """
    Returns whether or not a game exists.
    """
    return name in events


def get_events_dict():
    return events


def get_events():
    return list(events.keys())


def get_event_details(event):
    return events.get(event, None)


def add_event(name, details):
    if not isinstance(name, str):
        raise TypeError(f'Wrong type for name: {type(name)=}')
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    for field in REQUIRED_FLDS:
        if field not in details:
            raise ValueError(f'Required {field=} missing from details.')
    events[name] = details

def del_event(name):
    del events[name]


def main():
    events = get_events()
    print(f'{events=}')
    print(f'{get_event_details(TEST_EVENT_NAME)=}')


if __name__ == '__main__':
    main()