import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Define stock tickers
stocks = ['SPY', 'BTC-USD', 'ETH-USD', 'AAPL', 'MSFT', 'META', 'AMZN', 'GOOGL', 'NVDA', 'TSLA', 
          'JPM', 'V', 'JNJ', 'WMT', 'PG', 'XOM', 'BAC', 'HD', 'UNH', 'MA', 'INTC', 'VZ', 'DIS', 
          'NFLX', 'ADBE', 'CRM', 'CSCO']

# Function to get stock data
def get_stock_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)
    return data['Adj Close']

# Function to calculate daily returns
def calculate_returns(data):
    return data.pct_change()

# Function to plot stock performance
def plot_stock_performance(data, title):
    plt.figure(figsize=(12, 6))
    for column in data.columns:
        plt.plot(data.index, data[column], label=column)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)  # Added grid lines for better readability
    plt.show()

# Set date range
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

# Get stock data
stock_data = get_stock_data(stocks, start_date, end_date)

# Calculate returns
returns = calculate_returns(stock_data)

# Plot stock performance
plot_stock_performance(stock_data, 'Stock Performance Over the Last Year')

# Calculate and print summary statistics
summary = returns.describe()
print("Summary Statistics of Daily Returns:")
print(summary)

# Find best and worst performing stocks
best_stock = returns.mean().idxmax()
worst_stock = returns.mean().idxmin()

print(f"\nBest performing stock: {best_stock}")
print(f"Worst performing stock: {worst_stock}")

# Calculate correlation matrix
correlation_matrix = returns.corr()

# Plot correlation heatmap using seaborn
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5,
            xticklabels=correlation_matrix.columns, yticklabels=correlation_matrix.columns)
plt.title('Correlation Heatmap of Stock Returns')
plt.show()