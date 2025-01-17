


1. **Categorizes Stocks** into:
   - Bullish (sentiment > 0.1)
   - Bearish (sentiment < -0.1)
   - Neutral (-0.1 ≤ sentiment ≤ 0.1)

2. **Creates a Pie Chart** showing:
   - Distribution of bullish/bearish/neutral stocks
   - Percentage of stocks in each category
   - Color coding (green for bullish, red for bearish, gray for neutral)
   - Legend with actual stock tickers in each category

3. **Provides Detailed Output** including:
   - Category breakdown
   - Individual stock sentiment scores

Example usage:
```python
news_articles = [
    {'ticker': 'AAPL', 'text': 'positive article text...'},
    {'ticker': 'GOOGL', 'text': 'negative article text...'},
    {'ticker': 'MSFT', 'text': 'neutral article text...'},
    # ... more articles
]

main()
```

The output will be:
- A pie chart saved as 'sentiment_distribution_YYYYMMDD.png'
- Detailed console output showing each stock's category and sentiment score
- Logged information in 'sentiment_analysis_YYYYMMDD.log'

You can adjust the sentiment thresholds (currently ±0.1) in the `categorize_sentiment` function to make the categorization more or less sensitive to sentiment variations.
