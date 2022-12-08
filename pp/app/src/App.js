import './App.css';
import React, {useState} from 'react'

function App() {
  
  const [postalCode, setPostalCode] = useState('')
  const [maxPrice, setMaxPrice] = useState('')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [size, setSize] = useState('')
  const [events, setEvents] = useState([])

  const handleSubmit = async (evt) => {
    evt.preventDefault()
    try {
      const res = await fetch ("http://127.0.0.1:8000/get-events", {
      method: "POST",
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        postal_code: postalCode,
        max_price: maxPrice,
        start_date: startDate,
        end_date: endDate,
        size: size,
      })
      })
      const parsed = await res.json()
      if (res.status === 200) {
      setEvents(parsed.events)
      console.log(events)
      } else {
      console.log("GetEvents failed")
      }
    } catch (err) {
      console.log(err)
    }
  }

  return (
    <>
    <div className="App">
      <header className="App-header">
        <h1>Ticket Scraper</h1>
      </header>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          value={postalCode}
          placeholder="Postal Code"
          onChange={evt => setPostalCode(evt.target.value)}
        />
        <input
          type="number"
          value={maxPrice}
          placeholder="Max Price"
          onChange={evt => setMaxPrice(evt.target.value)}
        />
        From:
        <input
          type="date"
          value={startDate}
          onChange={evt => setStartDate(evt.target.value)}
        />
        To:
        <input
          type="date"
          value={endDate}
          onChange={evt => setEndDate(evt.target.value)}
        />
        <input
          type="number"
          value={size}
          placeholder="How many events?"
          onChange={evt => setSize(evt.target.value)}
        />
        <button type="submit">Search</button>
      </form>
      <div>
        {(events && events.length > 0) ?
        events.map(e => 
          <div>
            <p key={e.id}>Event name: {e.name}, Link: <a href={e.url} target="_blank">click here for more information!</a></p>
          </div>
        )
        :
        <p>No events found</p>}
      </div>
      <footer>
        <p>About: This event searcher searches for nearby events in the area. The options given to filter the events by Location, Date, Price, Venue, Artist, Genre, and Ticket Availability. This project was done to make nearby, local events more accessable to visitors, tourists , and people that are bored and are looking for fun things to do in the area. This website searches using SeatGeek and Ticketmaster to provide a streamline and one stop shop for events near you.</p>
      </footer>
    </div>
    </>
  );
}

export default App;
