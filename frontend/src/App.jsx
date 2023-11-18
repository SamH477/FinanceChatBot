import React, { useState, useEffect, useRef } from 'react';
import { Box, Heading, Input, Button, Container } from '@chakra-ui/react';
import { Link } from 'react-router-dom';
import Analysis from './Analysis';
import './style.css'; // Assuming you have style.css in your src folder

const App = () => {
    const [ticker, setTicker] = useState('');
    const [messages, setMessages] = useState([{ text: "Hello! I am a finance bot here to help you learn about stocks. What would you like to know?", from: "bot" }]);
    const [listening, setListening] = useState(false);
    const recognitionRef = useRef(null);

    useEffect(() => {
        // Speech recognition setup
        const recognition = new window.webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onresult = (event) => {
            let result = "";
            for (let i = event.resultIndex; i < event.results.length; i++) {
                if (event.results[i].isFinal) {
                    result += event.results[i][0].transcript;
                }
            }
            if (result.trim() !== '') {
                appendMessage(result, 'user');  // Append the voice message directly
                sendToServer(result, 'voice'); // Send the result to the server
            }
        };        

        recognition.onend = () => {
            setListening(false);
        };

        recognitionRef.current = recognition;
    }, []);

    const handleVoiceClick = () => {
    if (listening) {
        recognitionRef.current.stop();
    } else {
        recognitionRef.current.start();
    }
    setListening(!listening);
    
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (ticker.trim() !== '') {
            // Add the user's message as a bubble
            appendMessage(ticker, 'user');
    
            // Send the user's message to the server
            sendToServer(ticker, 'text');
            
            setTicker('');
        }
    };


    const appendMessage = (message, sender) => {
        setMessages(prevMessages => [...prevMessages, { text: message, from: sender }]);
    };    

    const sendToServer = async (data) => {
        try {
            const response = await fetch('http://localhost:5000/', {
                method: 'POST',
                body: data, // Send the audio data directly
            });
    
            if (response.ok) {
                const result = await response.json();
                const responseText = result.response;
                appendMessage(responseText, 'bot');
            } else {
                console.error('Request failed with status:', response.status);
            }
        } catch (error) {
            console.error('Error sending audio data:', error);
        }
    };

    return (
        <>
        <div className="top-link">
            <Link to="/analysis">Go to Analysis Page</Link>
        </div>
        <div className="chat-container" style={{ border: '8px solid white' }}> {/* Add this style */}
            <div className="chat-header">
                <h1 style={{ color: '#7dc0ff' }}>StockWhisper Analyst</h1>
            </div>
            <div className="chat-messages">
                {messages.map((message, index) => (
                    <div key={index} className={`message from-${message.from}`}>
                        <p>{message.text}</p>
                    </div>
                ))}
            </div>
            <div className="chat-input">
                <form onSubmit={handleSubmit}>
                    <input
                        type="text"
                        id="ticker"
                        name="ticker"
                        placeholder="Type your message..."
                        value={ticker}
                        onChange={(e) => setTicker(e.target.value)}
                        style={{ color: '#000' }} // Set text color to black
                    />
                </form>
                <button onClick={handleVoiceClick}>{listening ? "Listening..." : "🎤"}</button>
                <button onClick={handleSubmit}>Send</button>
            </div>
        </div>
        </>
    );
};

export default App;
