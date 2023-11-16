import datetime
import requests
import apiconfig
from textblob import TextBlob

# Use a list to store stocks for each ticker
ticker_to_stocks = {}

# Function to get sentiment data for a given ticker


def find_company(ticker):
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': ticker,
        'apikey': apiconfig.ALPHA_VANTAGE_API_KEY
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        companies = [
            {
                'symbol': result['1. symbol'],
                'name': result.get('2. name', '')
            }
            for result in data.get('bestMatches', [])
        ]
        return companies
    else:
        return []


# Function to fetch news articles for a stock using the News API
def fetch_news_for_ticker(ticker):
    base_url = 'https://newsapi.org/v2/everything'
    one_week_ago = (datetime.datetime.now() -
                    datetime.timedelta(days=7)).isoformat()

    params = {
        'q': ticker,  # Use ticker as the search query
        'apiKey': apiconfig.NEWS_API_KEY,
        'from': one_week_ago,  # Set the start date to one week ago
        # Set the end date to the current date
        'to': datetime.datetime.now().isoformat()
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])

        # Extract only the desired elements from each article
        simplified_news = [
            {
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'content': article.get('content', '')
            }
            for article in articles
        ]

        return simplified_news
    else:
        return []


# Function to analyze sentiment based on text


def analyze_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Function to recommend stocks based on the ticker and sentiment analysis


# Function to recommend stocks based on the ticker and sentiment analysis
# Function to recommend stocks based on the ticker and sentiment analysis
def recommend_stocks(ticker):
    # Find companies related to the given ticker
    companies = find_company(ticker)

    # Analyze sentiment for each company
    recommendations = []

    for company in companies:
        stock = company['symbol']
        company_name = company['name']

        # Analyze sentiment for each stock only if there are news articles
        news_articles = fetch_news_for_ticker(stock)

        if news_articles:
            sentiment_scores = []

            for article in news_articles:
                title_sentiment = analyze_sentiment(article.get('title', ''))
                description_sentiment = analyze_sentiment(
                    article.get('description', ''))
                content_sentiment = analyze_sentiment(
                    article.get('content', ''))

                # Append individual sentiment scores to the list
                sentiment_scores.extend(
                    [title_sentiment, description_sentiment, content_sentiment])

            # Calculate the average sentiment rounded to four decimal places
            if sentiment_scores:
                average_sentiment = round(
                    sum(sentiment_scores) / len(sentiment_scores), 4)
            else:
                average_sentiment = 0.0  # Default to 0 if no sentiment scores are available

            # Return a single recommendation with the average sentiment
            recommendations.append({
                "stock": stock,
                "company_name": company_name,
                "average_sentiment": average_sentiment
            })

    recommendations.sort(key=lambda x: x["average_sentiment"], reverse=True)

    return recommendations
