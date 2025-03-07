import axios from 'axios';
import React from 'react';
import './App.css';

function App() {
  const handleClick = () => {
    const textToSpeak = prompt("Enter text to speak:", "Hello from React!");
    if (textToSpeak) {
      axios.post('http://localhost:8000/api/speak/', { text: textToSpeak }) // backend url
        .then(response => {
          console.log(response.data.message); // Log success message
        })
        .catch(error => {
          console.error('Error speaking text:', error); // Log error
        });
    }
  };

  return (
    <div className="App">
      <h1>React Web App</h1>
      <button onClick={handleClick}>Speak Text</button>
    </div>
  );
}

export default App;