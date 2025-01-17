# scripts/preprocess_bias_data.py
import pandas as pd

df = pd.read_csv('data/bias_analysis/raw/tweets.csv')
df['clean_text'] = df['text'].str.replace(r'[^a-zA-Z\s]', '', regex=True).str.lower()
df.to_csv('data/bias_analysis/processed/tweets_clean.csv', index=False)