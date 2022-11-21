FILTER_ID = 'id'

REQUIRED_FLDS = [FILTER_ID]
filters = {'Location': {FILTER_ID: 0},
         'Date': {FILTER_ID: 1}, 
         'Price': {FILTER_ID: 2}, 
         'Venue': {FILTER_ID: 3},
         'Artist': {FILTER_ID: 4},
         'Venue': {FILTER_ID: 5}, 
         'Ticket Availability': {FILTER_ID: 6}, }


def filter_exists(name):
    return name in filters


def get_sort_values_dict():
    return filters


def get_filters():
    return list(filters.keys())

def main():
    filters = get_filters()
    print(f'{filters=}')
    
if __name__ == '__main__':
    main()