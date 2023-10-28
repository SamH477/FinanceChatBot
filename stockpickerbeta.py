import requests
import apiconfig
from textblob import TextBlob

sector_to_stocks = []

def get_available_sectors():
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'LIST_SECTORS',
        'apikey': apiconfig.ALPHA_VANTAGE_API_KEY
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        available_sectors = data.get('availableSectors', [])
        return available_sectors
    else:
        return []

def get_stocks_for_sector(sector):
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'SECTOR',
        'apikey': apiconfig.ALPHA_VANTAGE_API_KEY,
        'sector': sector  # Include the sector parameter in the request
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()

        if 'Rank A: Real-Time Performance' in data:
            sector_data = data['Rank A: Real-Time Performance']
            stocks = [item['symbol'] for item in sector_data if item['sector'] == sector]
            return stocks
        else:
            return None
    else:
        return None


def update_sector_stocks():
    available_sectors = get_available_sectors()

    for sector in available_sectors:
        fetched_stocks = get_stocks_for_sector(sector)
        if fetched_stocks:
            sector_to_stocks[sector] = fetched_stocks

# Call the function to update sectors with their associated stocks
update_sector_stocks()

# Function to fetch news articles for a stock using the News API.
def fetch_news_for_stock(stock):
    base_url = 'https://newsapi.org/v2/everything'
    params = {
        'q': stock,            # Stock symbol as the search query
        'apiKey': apiconfig.NEWS_API_KEY
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        return articles
    else:
        return []
    
def analyze_sentiment(text):
    analysis = TextBlob(text)

    return analysis.sentiment.polarity

# Function to recommend stocks based on sector and sentiment analysis.
def recommend_stocks(sector):
    if sector not in sector_to_stocks:
        return "Sorry, I don't have information for that sector."

    sector_stocks = sector_to_stocks[sector]
    recommendations = []
    print(sector_stocks)
    for stock in sector_stocks:
        news_articles = fetch_news_for_stock(stock)
        sentiment_scores = [analyze_sentiment(article['title']) for article in news_articles]
        average_sentiment = sum(sentiment_scores) / max(len(sentiment_scores), 1)

        recommendations.append({
            "stock": stock,
            "average_sentiment": average_sentiment
        })
    print(recommendations)

    recommendations.sort(key=lambda x: x["average_sentiment"], reverse=True)

    return recommendations