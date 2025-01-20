from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from textblob import TextBlob
import nltk

nltk.download('punkt')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the Twitter API Bearer Token from an environment variable
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

def get_tweets(topic):
    """
    Fetch recent tweets about the given topic from verified accounts.
    """
    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}',
    }
    params = {
        'query': f'"{topic}" is:verified lang:en',
        'max_results': 100,
    }
    url = 'https://api.twitter.com/2/tweets/search/recent'

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error fetching tweets: {response.status_code} {response.text}")
        return []
    tweets_data = response.json()
    tweets = tweets_data.get('data', [])
    return tweets

def analyze_sentiment(tweets):
    """
    Analyze the sentiment of tweets and classify them as positive, negative, or neutral.
    """
    sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}
    for tweet in tweets:
        text = tweet.get('text', '')
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity

        if polarity > 0.05:
            sentiments['positive'] += 1
        elif polarity < -0.05:
            sentiments['negative'] += 1
        else:
            sentiments['neutral'] += 1

    total = sum(sentiments.values())
    if total == 0:  # Avoid division by zero
        return {'positive': 0, 'negative': 0, 'neutral': 0}

    for key in sentiments:
        sentiments[key] = round((sentiments[key] / total) * 100, 2)
    return sentiments

def calculate_social_engagement(tweets):
    """
    Placeholder function to calculate social engagement from tweets.
    Returns the number of tweets as a proxy for engagement.
    """
    return len(tweets)

@app.route('/analyze')
def analyze():
    """
    Endpoint to analyze sentiment and metrics for a given topic.
    """
    topic = request.args.get('topic')
    if not topic:
        return jsonify({'error': 'No topic provided.'}), 400

    tweets = get_tweets(topic)
    sentiments = analyze_sentiment(tweets)
    metrics = {
        'approval': sentiments.get('positive', 0),
        'media_coverage': len(tweets),
        'social_engagement': calculate_social_engagement(tweets)
    }

    return jsonify({'sentiments': sentiments, 'metrics': metrics})

if __name__ == '__main__':
    # Set debug to False in production
    app.run(debug=True)