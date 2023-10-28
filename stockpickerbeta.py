import requests
import apiconfig
from textblob import TextBlob

# Use a list to store stocks for each ticker
ticker_to_stocks = {}

# Function to get sentiment data for a given ticker
def get_sentiment(ticker):
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': ticker,
        'apikey': apiconfig.ALPHA_VANTAGE_API_KEY
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        stocks = [result['1. symbol'] for result in data.get('bestMatches', [])]
        return stocks
    else:
        return []

# Function to fetch news articles for a stock using the News API
def fetch_news_for_ticker(ticker):
    base_url = 'https://newsapi.org/v2/everything'
    params = {
        'q': ticker,  # Use ticker as the search query
        'apiKey': apiconfig.NEWS_API_KEY
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        return articles
    else:
        return []

# Function to analyze sentiment based on text
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Function to recommend stocks based on the ticker and sentiment analysis
def recommend_stocks(ticker):
    available_stocks = get_sentiment(ticker)

    if not available_stocks:
        return "Sorry, I don't have information for that ticker."

    ticker_to_stocks[ticker] = available_stocks

    recommendations = []

    for stock in available_stocks:
        news_articles = fetch_news_for_ticker(stock)
        sentiment_scores = [analyze_sentiment(article['title']) for article in news_articles]
        average_sentiment = sum(sentiment_scores) / max(len(sentiment_scores), 1)

        recommendations.append({
            "stock": stock,
            "average_sentiment": average_sentiment
        })

    recommendations.sort(key=lambda x: x["average_sentiment"], reverse=True)

    return recommendations

