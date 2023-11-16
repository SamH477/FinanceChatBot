import React, { useState, useRef } from 'react';
import { Box, Heading, Input, Button, Container, Flex } from '@chakra-ui/react';
import StockRecommendations from './components/recommend';

const Analysis = () => {
  const [ticker, setTicker] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [showRecommendations, setShowRecommendations] = useState(false);
  const [listening, setListening] = useState(false);
  const [buttonText, setButtonText] = useState('🎤');

  const recognitionRef = useRef(null);

  const handleSpeechRecognitionClick = () => {
    if (!listening) {
      startSpeechRecognition();
    } else {
      stopSpeechRecognition();
    }
  };

  const startSpeechRecognition = () => {
    if (!recognitionRef.current) {
      recognitionRef.current = new window.webkitSpeechRecognition();
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;

      recognitionRef.current.onresult = (event) => {
        let result = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            result += event.results[i][0].transcript;
          }
        }
        setTicker(result.trim());
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
      };

      recognitionRef.current.onend = () => {
        setListening(false);
        // Update button text when recognition is stopped
        setButtonText('🎤');
      };
    }

    recognitionRef.current.start();
    setListening(true);
    // Update button text when recognition is started
    setButtonText('...');
  };

  const stopSpeechRecognition = () => {
    // Stop the current SpeechRecognition instance
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    setListening(false);
    // Update button text when recognition is stopped
    setButtonText('🎤');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/recommend', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ticker }),
      });

      if (response.ok) {
        const data = await response.json();
        setRecommendations(data);
        setShowRecommendations(true);
      } else {
        console.error('Request failed with status:', response.status);
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
  };

  return (
    <Container 
      centerContent 
      maxW="container.md" 
      p={5} 
      backgroundColor="#ddf57d" 
      borderRadius="15px"
      boxShadow="lg"
      border="8px solid"
      borderColor="black.500"
    >
      <Box textAlign="center" w="100%">
        <Heading as="h1" color="#7dc0ff">StockWhisper Analyst</Heading>
        <form onSubmit={handleSubmit}>
          <label htmlFor="ticker" style={{ color: '#7dc0ff' }}>Enter a company or stock ticker:</label>
          <Input
            type="text"
            id="ticker"
            name="ticker"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            mb={3}
            color="#7dc0ff"
          />
          <Flex justify="center" gap="2"> {/* Flex container for buttons */}
            <Button type="submit" colorScheme="blue">Analyze</Button>
            <Button onClick={handleSpeechRecognitionClick} colorScheme="green">
              {buttonText}
            </Button>
          </Flex>
        </form>

        {showRecommendations && (
          <StockRecommendations recommendations={recommendations} />
        )}
      </Box>
    </Container>
  );
};

export default Analysis;
