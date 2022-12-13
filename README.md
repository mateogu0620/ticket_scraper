# TicketScraper

To create the env for a new developer, run `make dev_env`.
To run the server and interact with the swagger api, run `./local.sh`
To run the tests, run `make unit`

This is a flask rest API server that searches for nearby converts (from Ticketmaster and Seatgeek) and stores and presents them to users. The goal is to make a website that helps users find new and exciting events near them to explore in a single place.


## Requirements

Lists events/concerts based on a set of filters
Filters:
    Location
    Date Range
    Price

Links event/concerts to their according site where we got the information from

## Design

UI has basic search interface, scraper will collect events from nearby from Ticketmaster and Seatgeek

Database and table schema for “ticket prices” / “events”:
- Have updating table with new events coming in, with primary key EVENT_ID
- Additional tables based on genre (potentially designated TS_CONCERT_METAL, or TS_CONCERT_RNB or TS_COMEDY_SAMMORRIL)
- Table columns should include venue field so “nearby” concerts included

Main mechanism is Ticketmaster and Seatgeek APIs are called and our database is populated with events. These events
are then displayed on the page or returned as a collection of events from the API.

## Tests

- Tests getting events from Ticketmaster (1 test)
- Tests getting events from Seatgeek (1 test)
- Tests getting events from both Ticketmaster and Seatgeek (1 test)
- Test basic insert, get, and delete mongo db operations (8 tests)

## UI

UI is a simple, minimalistic web-based user interface, primarily centered around the search interface, which will 
input a location, date range, and price preferences, and will return the concert tickets that fullfill the search data.
In the future, there will be the option to filter tickets based on certain filter or optionally by which API's are being called, as well as sort events by a particular field.

The search interface will have buttons and a drop-down menu to select the filters from a pre-determined list, and optionally may include a Google maps window with the location pins of the nearby concerts overlaid on top.

## Relevant APIs

SeatGeek https://platform.seatgeek.com/

TicketMaster https://developer.ticketmaster.com/products-and-docs/apis/getting-started/
