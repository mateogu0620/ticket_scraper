import './App.css';
import React, {useState,useEffect} from 'react'

function App() {
  
  const [data,setData] = useState([{}])

  useEffect(() => { fetch("/test_eventreact").then(
    res=>res.json()
    ).then(data => {
      setData(data)
      console.log(data)
    })},[])
  useEffect(() => { fetch("/tm_get_events").then(
    res=>res.json()
    ).then(data => {
      setData(data)
      console.log(data)
    })},[])
  
  return (
    <div className="App">
      <header className="App-header">
        <h1>Ticket Scraper</h1>
        <table id="customers">
        <tr>
          <th>Event Name</th>
          <th>Location</th>
          <th>Date</th>
          <th>Price</th>
          <th>Venue</th>
          <th>Artist</th>
          <th>Genre</th>
          <th>Ticket Availability</th>
        </tr>
        
        <tr>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
        </tr>
        <tr>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
        </tr>
      </table>
        
        <p>About: This event searcher searches for nearby events in the area. The options given to filter the events by Location, Date, Price, Venue, Artist, Genre, and Ticket Availability. This project was done to make nearby, local events more accessable to visitors, tourists , and people that are bored and are looking for fun things to do in the area. This website searches using SeatGeek and Ticketmaster to provide a streamline and one stop shop for events near you.</p>

      </header>
      <div>
        {(typeof data.events == 'undefined') ? (
          <p>Error</p>
        ):(
          data.events.map((event,i) => (
            <p key={i}>{event}</p>
          ))
        )}
      </div>
    </div>

  );
}

export default App;
