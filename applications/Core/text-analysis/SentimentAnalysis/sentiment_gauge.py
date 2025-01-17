import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Dict, List
import logging
from datetime import datetime
import numpy as np
from textblob import TextBlob

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=f'sentiment_analysis_{datetime.now().strftime("%Y%m%d")}.log'
)

def calculate_sentiment_scores(news_articles: List[Dict]) -> pd.DataFrame:
    """Calculate and categorize sentiment scores for news articles."""
    try:
        scores = {}
        for article in news_articles:
            ticker = article['ticker']
            text = article['text']
            
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity
            
            if ticker not in scores:
                scores[ticker] = []
            scores[ticker].append(sentiment)
            
        df = pd.DataFrame(scores)
        logging.info(f"Successfully calculated sentiment scores for {len(news_articles)} articles")
        return df
        
    except Exception as e:
        logging.error(f"Error calculating sentiment scores: {str(e)}")
        raise

def categorize_sentiment(scores: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Categorize stocks into bullish or bearish based on average sentiment.
    
    Args:
        scores: DataFrame containing sentiment scores
        
    Returns:
        Dictionary with 'bullish' and 'bearish' lists of stocks
    """
    try:
        mean_sentiments = scores.mean()
        sentiment_categories = {
            'bullish': [],
            'bearish': [],
            'neutral': []  # Optional: for scores very close to 0
        }
        
        for ticker, sentiment in mean_sentiments.items():
            if sentiment > 0.1:  # Bullish threshold
                sentiment_categories['bullish'].append(ticker)
            elif sentiment < -0.1:  # Bearish threshold
                sentiment_categories['bearish'].append(ticker)
            else:
                sentiment_categories['neutral'].append(ticker)
                
        return sentiment_categories
        
    except Exception as e:
        logging.error(f"Error categorizing sentiments: {str(e)}")
        raise

def plot_sentiment_distribution(sentiment_categories: Dict[str, List[str]]) -> None:
    """
    Create pie chart of bullish vs bearish sentiment distribution.
    
    Args:
        sentiment_categories: Dictionary containing categorized stocks
    """
    try:
        # Calculate sizes for pie chart
        sizes = [len(stocks) for stocks in sentiment_categories.values()]
        labels = [f"{category.title()}\n({len(stocks)} stocks)" 
                 for category, stocks in sentiment_categories.items()]
        
        # Color mapping
        colors = ['#2ecc71', '#e74c3c', '#95a5a6']  # Green for bullish, Red for bearish, Gray for neutral
        
        # Create pie chart
        plt.figure(figsize=(12, 8))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
                startangle=90, pctdistance=0.85)
        
        # Add title
        plt.title('Market Sentiment Distribution', pad=20, size=16)
        
        # Add legend with stock tickers
        legend_labels = []
        for category, stocks in sentiment_categories.items():
            stocks_str = ', '.join(stocks) if stocks else 'None'
            legend_labels.append(f"{category.title()}: {stocks_str}")
        
        plt.legend(legend_labels, 
                  title="Stocks by Sentiment Category",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))
        
        plt.savefig(f'sentiment_distribution_{datetime.now().strftime("%Y%m%d")}.png',
                   bbox_inches='tight')
        logging.info("Successfully created sentiment distribution pie chart")
        
    except Exception as e:
        logging.error(f"Error creating pie chart: {str(e)}")
        raise

def main():
    try:
        # Calculate sentiment scores
        sentiment_scores = calculate_sentiment_scores(news_articles)
        
        # Categorize sentiments
        sentiment_categories = categorize_sentiment(sentiment_scores)
        
        # Create pie chart
        plot_sentiment_distribution(sentiment_categories)
        
        # Print detailed results
        print("\nSentiment Analysis Results:")
        print("==========================")
        for category, stocks in sentiment_categories.items():
            print(f"\n{category.title()} Stocks:")
            if stocks:
                for stock in stocks:
                    avg_sentiment = sentiment_scores[stock].mean()
                    print(f"{stock}: {avg_sentiment:.3f}")
            else:
                print("None")
        
        logging.info("Sentiment analysis completed successfully")
        
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()