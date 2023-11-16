import React, { useState, useEffect, useRef } from 'react';
import { Box, Heading, Input, Button, Container } from '@chakra-ui/react';
import { Link } from 'react-router-dom';
import Analysis from './Analysis';
import './style.css'; // Assuming you have style.css in your src folder

const App = () => {
    const [ticker, setTicker] = useState('');
    const [messages, setMessages] = useState([{ text: "Hello! Ask me what stocks to invest in?", from: "bot" }]);
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
            setTicker(result);
            appendMessage(result, 'user');
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
            appendMessage(ticker, 'user');
            setTicker('');
            sendToServer(ticker);
        }
    };

    const appendMessage = (message, sender) => {
        setMessages([...messages, { text: message, from: sender }]);
    };

    const sendToServer = (data) => {
        // Your fetch logic here
    };

    return (
        <>
        <div className="top-link">
                <Link to="/analysis">Go to Analysis Page</Link>
            </div>
        <div className="chat-container">
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
