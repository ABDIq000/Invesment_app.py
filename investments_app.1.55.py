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

# Predefined list of big companies
def get_big_companies():
    return [
        ("Apple", "AAPL"),
        ("Microsoft", "MSFT"),
        ("Amazon", "AMZN"),
        ("Tesla", "TSLA"),
        ("Google", "GOOGL"),
        ("NVIDIA", "NVDA"),
        ("Meta Platforms", "META"),
        ("Netflix", "NFLX"),
    ]

# Fetch smaller companies predicted to rise
def get_rising_companies():
    try:
        # Example: Use Yahoo Finance or Finnhub for real-time trending stocks
        # Replace this with an actual API call to fetch trending small/mid-cap stocks
        return [
            ("Rivian", "RIVN"),
            ("Lucid Motors", "LCID"),
            ("Palantir", "PLTR"),
            ("Zoom Video", "ZM"),
        ]
    except:
        return []

# Streamlit app
def main():
    st.title("Investment Recommendation App")
    st.write("Analyze big company stocks and dynamically add smaller companies predicted to rise.")
    
    # User input for NewsAPI key
    api_key = st.text_input("Enter your NewsAPI key", type="password")
    
    if st.button("Analyze"):
        if not api_key:
            st.error("Please enter your NewsAPI key.")
            return
        
        # Fetch big companies and rising companies
        big_companies = get_big_companies()
        rising_companies = get_rising_companies()
        stocks = big_companies + rising_companies
        
        st.write("Analyzing stocks...")
        recommendations = []
        
        # Analyze all stocks
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
                    "Category": "Big Company" if (stock_name, stock_symbol) in big_companies else "Rising Company"
                })
        
        # Display recommendations
        if recommendations:
            st.success("Recommended Stocks:")
            st.table(recommendations)
        else:
            st.warning("No stocks recommended based on the sentiment analysis.")

if __name__ == "__main__":
    main()