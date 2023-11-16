import React from 'react';
import { Box, Heading, Link, Badge } from '@chakra-ui/react';

const StockRecommendations = ({ recommendations }) => {
  return (
    <Box textAlign="center">
      <Heading 
      as="h1" 
      fontSize="1.5rem" 
      color="#7dc0ff" // Setting the color
      >Sentiment Analysis:</Heading>

      {recommendations && recommendations.length > 0 ? (
        <>
          {recommendations.map((recommendation, index) => (
            <Box
              key={index}
              borderWidth="1px"
              borderRadius="lg"
              p={4}
              mb={4}
              borderColor="gray.300"
              bg="gray.200"
              color="#7dc0ff"
            >
              <Box fontSize="lg" fontWeight="bold">
                Company: {recommendation.company_name}
              </Box>
              <Box>
                Ticker: {recommendation.stock}
                <br />
                Average Sentiment: {recommendation.average_sentiment}
              </Box>
              <Badge
                colorScheme={
                  recommendation.average_sentiment > 0.10
                    ? "green"
                    : recommendation.average_sentiment < -0.10
                    ? "red"
                    : "gray"
                }
                fontWeight="bold"
                mt={2}
              >
                {recommendation.average_sentiment > 0.10
                  ? "Bullish"
                  : recommendation.average_sentiment < -0.10
                  ? "Bearish"
                  : "Neutral"}
              </Badge>
            </Box>
          ))}
        </>
      ) : (
        <p style={{ color: "#7dc0ff" }}>Ticker not found.</p>
      )}

      <Link href="/">Go to Home</Link>
    </Box>
  );
};

export default StockRecommendations;
