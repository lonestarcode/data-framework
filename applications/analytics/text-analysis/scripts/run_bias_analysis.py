# scripts/run_bias_analysis.py
import pandas as pd
from models.bias_analysis.bias_detection import analyze_bias

df = pd.read_csv('data/bias_analysis/processed/tweets_clean.csv')
results = analyze_bias(df['clean_text'].tolist())
pd.DataFrame(results).to_csv('data/bias_analysis/analysis_logs/bias_results.csv', index=False)