# models/sentiment_analysis/sentiment_model.py
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def analyze_sentiment(texts):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)
    model = MultinomialNB()
    model.fit(X, [0 if i % 2 == 0 else 1 for i in range(len(texts))])
    predictions = model.predict(X)
    return [{'text': text, 'sentiment': 'positive' if pred == 1 else 'negative'} for text, pred in zip(texts, predictions)]