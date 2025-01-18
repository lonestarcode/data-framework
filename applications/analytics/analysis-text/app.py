# app.py
import pandas as pd
from models.bias_analysis.bias_detection import analyze_bias
from models.sentiment_analysis.sentiment_model import analyze_sentiment
from models.language_detection.language_model import detect_language
from models.topic_modeling.topic_model import analyze_topics
from models.topic_modeling.config import NUM_TOPICS
import requests
import json

def main():
    # Load data
    df = pd.read_csv('data/raw/texts.csv')
    texts = df['text'].tolist()

    # Run all analyses
    bias_results = analyze_bias(texts)
    sentiment_results = analyze_sentiment(texts)
    language_results = detect_language(texts)
    topic_results = analyze_topics(texts, NUM_TOPICS)

    # Save results
    pd.DataFrame(bias_results).to_csv('data/analysis_logs/bias_results.csv', index=False)
    pd.DataFrame(sentiment_results).to_csv('data/analysis_logs/sentiment_results.csv', index=False)
    pd.DataFrame(language_results).to_csv('data/analysis_logs/language_results.csv', index=False)
    pd.DataFrame(topic_results).to_csv('data/analysis_logs/topic_results.csv', index=False)

    print("Analysis complete. Results saved to data/analysis_logs/")

if __name__ == "__main__":
    main()

# Language Detection
response = requests.post('http://localhost:5001/detect_language',
                        json={'texts': ['Hello world', 'Bonjour monde']})
print(json.dumps(response.json(), indent=2))

# Sentiment Analysis
response = requests.post('http://localhost:5002/analyze_sentiment',
                        json={'texts': ['I love this!', 'This is terrible']})
print(json.dumps(response.json(), indent=2))

# Topic Analysis
response = requests.post('http://localhost:5003/analyze_topics',
                        json={'texts': ['AI and machine learning', 'Sports and games'],
                              'n_topics': 2})
print(json.dumps(response.json(), indent=2))

# Bias Analysis
response = requests.post('http://localhost:5000/analyze_bias',
                        json={'texts': ['This is a neutral statement', 'This group always does that']})
print(json.dumps(response.json(), indent=2))