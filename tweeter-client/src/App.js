import React, {useEffect, useState} from 'react';
import './App.css';


const loadTweets = function(callback) {

  const xhr = new XMLHttpRequest()
  const method = 'GET'
  const url = 'http://localhost:8000/api/tweets/'
  const responseType = 'json'

  xhr.responseType = responseType
  xhr.open(method, url)
  xhr.onload = function(){
      callback(xhr.response, xhr.status)

  }
  xhr.onerror = function (e) {
    console.log(e)
    callback({"message": "there was error on request"}, 400)
  }
  xhr.send()

}

function App() {
  const [tweets, setTweets] = useState([])

  useEffect(() => {

    const myCallback = (response, status) => {
      if(status === 200){
        setTweets(response)
        console.log(tweets)
      } else {
        alert('there was an error')
      }
    }
    loadTweets(myCallback)

    
  }, [])

  return (
    <div className="App">
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */}
      {tweets.map((tweet, i) => {
        return <p key={i}>{tweet.content}</p>
      })}
    </div>
  );
}

export default App;
