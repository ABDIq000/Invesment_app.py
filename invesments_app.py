import streamlit as st
import requests
from textblob import TextBlob
import yfinance as yf
import pandas as pd

# Function to fetch news articles
def fetch_news(stock_name, api_key):
    url = f"https://newsapi.org/v2/everything?q={stock_name}&sortBy=publishedAt&apiKey={api_key}"
    response = requests.get(url)
    return response.json().get('articles', [])

# Function to analyze sentiment
def analyze_sentiment(articles):
    sentiments = []
    for article in articles:
        title = article.get('title', '')
        description = article.get('description', '')
        content = title + ' ' + description
        sentiment = TextBlob(content).sentiment.polarity  # Polarity ranges from -1 to 1
        sentiments.append(sentiment)
    return sum(sentiments) / len(sentiments) if sentiments else 0

# Function to get stock data
def get_stock_data(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    data = stock.history(period="1d")
    return data['Close'].iloc[-1] if not data.empty else None

# Predefined list of popular stocks
def get_popular_stocks():
    return [
        ("Apple", "AAPL"),
        ("Tesla", "TSLA"),
        ("Amazon", "AMZN"),
        ("Microsoft", "MSFT"),
        ("Google", "GOOGL"),
        ("NVIDIA", "NVDA"),
        ("Meta Platforms", "META"),
        ("Netflix", "NFLX"),
    ]

# Fetch senator-traded stocks
def get_senator_stocks():
    try:
        # Fetch data from Quiver Quantitative's API (or other sources)
        url = "https://www.quiverquant.com/beta/senate_trading"
        response = requests.get(url)
        data = response.json()
        
        # Extract stock symbols and names
        senator_trades = pd.DataFrame(data)
        senator_trades = senator_trades[['ticker', 'company']].drop_duplicates().head(10)
        return list(senator_trades.itertuples(index=False, name=None))  # Convert to list of tuples
    except:
        return []

# Streamlit app
def main():
    st.title("Investment Recommendation App")
    st.write("Analyze news sentiment, senator investments, and stock performance to make decisions.")
    
    # User input for NewsAPI key
    api_key = st.text_input("Enter your NewsAPI key", type="password")
    
    if st.button("Analyze"):
        if not api_key:
            st.error("Please enter your NewsAPI key.")
            return
        
        # Fetch popular stocks and senator stocks
        stocks = get_popular_stocks()
        senator_stocks = get_senator_stocks()
        
        st.write("Analyzing popular stocks...")
        recommendations = []
        
        # Analyze popular stocks
        for stock_name, stock_symbol in stocks:
            st.write(f"Analyzing {stock_name} ({stock_symbol})...")
            articles = fetch_news(stock_name, api_key)
            sentiment_score = analyze_sentiment(articles)
            current_price = get_stock_data(stock_symbol)
            
            if sentiment_score > 0:
                recommendations.append({
                    "Stock": stock_name,
                    "Symbol": stock_symbol,
                    "Sentiment Score": round(sentiment_score, 2),
                    "Current Price": current_price,
                    "Category": "Popular Stock"
                })
        
        # Analyze senator stocks
        st.write("Analyzing stocks traded by senators...")
        for stock_symbol, stock_name in senator_stocks:
            st.write(f"Analyzing {stock_name} ({stock_symbol})...")
            articles = fetch_news(stock_name, api_key)
            sentiment_score = analyze_sentiment(articles)
            current_price = get_stock_data(stock_symbol)
            
            if sentiment_score > 0:
                recommendations.append({
                    "Stock": stock_name,
                    "Symbol": stock_symbol,
                    "Sentiment Score": round(sentiment_score, 2),
                    "Current Price": current_price,
                    "Category": "Senator-Traded Stock"
                })
        
        # Display recommendations
        if recommendations:
            st.success("Recommended Stocks:")
            st.table(recommendations)
        else:
            st.warning("No stocks recommended based on the sentiment analysis.")

if __name__ == "__main__":
    main()