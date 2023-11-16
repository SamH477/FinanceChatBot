import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import App from './App.jsx';
import Analysis from './Analysis.jsx'; // Import your Analysis component
import './index.css';

const handleShowVoiceRecognition = () => {
  const voiceRecognitionIframe = document.querySelector('iframe[title="VoiceRecognition"]');
  if (voiceRecognitionIframe) {
    voiceRecognitionIframe.style.display = 'block';
  }
};

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App showVoiceRecognition={handleShowVoiceRecognition} />} />
        <Route path="/analysis" element={<Analysis />} />
      </Routes>
    </Router>
  </React.StrictMode>
);
