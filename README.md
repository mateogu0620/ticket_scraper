# TicketScraper

To build production, type `make prod`.

To create the env for a new developer, run `make dev_env`.

A flask rest API server that searches for nearby converts(from Ticketmaster, EventBrite, SeatGeek, etc) and stores and presents them to users. We also allow users to filter events based on factors such as user’s location, preferred genre, ticket prices , etc..

The goal is to make a website that helps users find new and exciting events near them to explore in a single place.


## Requirements

List events/concerts based on a set of filters

Potential Filters:
    Location
    Date
    Price
    Venue
    Artist
    Genre
    Ticket Availability

Allow viewing and sorting events by a given filter

Link event/concerts to their according site where we got the information from

## Design

UI has basic search interface, input genre and location (zip code?) and scraper will collect events from
nearby from EventBrite, SeatGeek, TicketMaster, etc. 

Database and table schema for “ticket prices” / “events”:
- Have updating table with new events coming in, with primary key EVENT_ID
- Additional tables based on genre (potentially designated TS_CONCERT_METAL, or TS_CONCERT_RNB or TS_COMEDY_SAMMORRIL)
- Table columns should include venue field so “nearby” concerts included

Potentially we use a scraper to fill out the database constantly, then query for every usage. Or, instead we call the API on every usage, and simply use the results from each. A combination of both might be good as well.

## Tests

- Basic tests (hello, etc)
- Test each API call (simple calls)
- Test if scraper is returning valid data with valid schema
- Test if the DB is filling out (scraper is loading data into tables)
- Reset test tables for each test. Maybe keep count of test run #? (this isn't necessary, probably)

## UI

UI is a simple, minimalistic web-based user interface, primarily centered around the search interface, which will 
input a musical genre and location and return the concert tickets that fullfill the search data. The default will 
return events from all three ticketing API's, with the option to filter tickets based on certain filter or optionally
by which API's are being called. This design will be handled with simple http templates handled on the Flask server backend.

The search interface will have buttons and a drop-down menu to select the filters from a pre-determined list, and optionally may
include a Google maps window with the location pins of the nearby concerts overlaid on top.

## Relevant APIs

GitHub - https://github.com/public-apis/public-apis: A collective list of free APIs

EventBrite https://www.eventbrite.com/platform/api/

SeatGeek https://platform.seatgeek.com/

TicketMaster https://developer.ticketmaster.com/products-and-docs/apis/getting-started/
