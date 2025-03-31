import axios from 'axios';
import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [backendData, setBackendData] = useState(null);
  const [isDataLoading, setIsDataLoading] = useState(true); // Add a loading state

  const handleClick = () => {
    const textToSpeak = prompt("Enter text to speak:", "Hello from React!");
    if (textToSpeak) {
      axios.post('http://localhost:8000/api/speak/', { text: textToSpeak })
        .then(response => {
          console.log(response.data.message);
          // Optionally, you could trigger a data refresh here after speaking
          // fetchData(); 
        })
        .catch(error => {
          console.error('Error speaking text:', error);
        });
    }
  };

  const fetchData = async () => {
    setIsDataLoading(true); // Set loading to true before fetching
    try {
      const response = await axios.get('http://localhost:8000/api/data/');
      setBackendData(response.data.message);
    } catch (error) {
      console.error('Error fetching data:', error);
      setBackendData("Error loading data");
    } finally {
      setIsDataLoading(false); // Set loading to false after fetching (success or error)
    }
  };

  useEffect(() => {
    fetchData(); // Initial fetch

    // Set up an interval to fetch data periodically
    const intervalId = setInterval(fetchData, 5000); // Fetch data every 5 seconds (adjust as needed)

    // Clean up the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, []); // Empty dependency array means this effect runs once on mount and cleanup on unmount

  return (
    <div className="App">
      <h1>React Web App</h1>
      <button onClick={handleClick}>Speak Text</button>
      <h1>Data from Backend:</h1>
      {isDataLoading ? (
        <p>Loading data...</p>
      ) : backendData ? (
        <p>{backendData}</p>
      ) : (
        <p>No data available.</p>
      )}
    </div>
  );
}

export default App;
