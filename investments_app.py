import streamlit as st
import requests
from textblob import TextBlob
import yfinance as yf

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

# Streamlit app
def main():
    st.title("Investment Recommendation App")
    st.write("Analyze news sentiment and stock performance to make investment decisions.")
    
    # User input
    api_key = st.text_input("Enter your NewsAPI key", type="password")
    stock_list = st.text_area(
        "Enter stocks to analyze (one per line in 'Name,Symbol' format):",
        "Apple,AAPL\nTesla,TSLA\nAmazon,AMZN"
    )
    
    if st.button("Analyze"):
        if not api_key:
            st.error("Please enter your NewsAPI key.")
            return
        
        stocks = [line.split(",") for line in stock_list.splitlines()]
        recommendations = []
        
        for stock_name, stock_symbol in stocks:
            st.write(f"Analyzing {stock_name} ({stock_symbol})...")
            articles = fetch_news(stock_name, api_key)
            sentiment_score = analyze_sentiment(articles)
            current_price = get_stock_data(stock_symbol)
            
            if sentiment_score > 0:
                recommendations.append({
                    "Stock": stock_name,
                    "Symbol": stock_symbol,
                    "Sentiment Score": sentiment_score,
                    "Current Price": current_price
                })
        
        if recommendations:
            st.success("Recommended Stocks:")
            st.table(recommendations)
        else:
            st.warning("No stocks recommended based on the sentiment analysis.")

if __name__ == "__main__":
    main()