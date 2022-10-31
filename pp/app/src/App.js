import './App.css';

function App() {
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
        
        <p>About: This event searcher searches for nearby events in the area. The options given to filter the events by Location, Date, Price, Venue, Artist, Genre, and Ticket Availability. This project was done to make nearby, local events more accessable to visitors, tourists , and people that are bored and are looking for fun things to do in the area. This website searches using SeatGeek and Ticketmaster to provide a streamline and one stop shop for events near you.


        </p>

      </header>
    </div>
  );
}

export default App;
