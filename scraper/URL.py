URL_NAME = 'test'
NAME = 'name'
URL_ID = 'id'

REQUIRED_FLDS = [URL_ID]
url = {URL_NAME: {URL_ID: 0},
         'settings': {URL_ID: 1},
         'logout': {URL_ID: 1}, }


def url_exists(name):
    """
    Returns whether or not a url exists.
    """
    return name in url


def get_url_dict():
    return url


def get_url():
    return list(url.keys())


def get_url_details(u):
    return url.get(u, None)


def add_url(name, details):
    if not isinstance(name, str):
        raise TypeError(f'Wrong type for name: {type(name)=}')
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    for field in REQUIRED_FLDS:
        if field not in details:
            raise ValueError(f'Required {field=} missing from details.')
    url[name] = details


def del_url(name):
    del url[name]


def main():
    url = get_url()
    print(f'{url=}')
    print(f'{get_url_details(URL_NAME)=}')


if __name__ == '__main__':
    main()