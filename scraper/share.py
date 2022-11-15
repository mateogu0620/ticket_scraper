TEST_SHARE_NAME = 'Test share'
NAME = 'name'
IMAGE = 'image'
URL = 'url'



# We expect the user database to change frequently:
# For now, we will consider EMAIL to be
# our mandatory fields.
REQUIRED_FLDS = [IMAGE,URL]
sites = {TEST_SHARE_NAME: {IMAGE: 'example.png', URL: 'example.com'},
         'twitter': {IMAGE: 'twitter.png', URL: 'twitter.com'}}


def share_exists(name):
    """
    Returns whether or not a user exists.
    """
    return name in sites


def get_sites():
    return list(sites.keys())


def get_sites_dict():
    return sites


def get_site_details(site):
    return sites.get(site, None)


def del_site(name):
    del sites[name]


def add_site(name, details):
    if not isinstance(name, str):
        raise TypeError(f'Wrong type for name: {type(name)=}')
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    for field in REQUIRED_FLDS:
        if field not in details:
            raise ValueError(f'Required {field=} missing from details.')
    sites[name] = details


def main():
    sites = get_sites()
    print(f'{sites=}')
    print(f'{get_site_details(TEST_SHARE_NAME)=}')


if __name__ == '__main__':
    main()