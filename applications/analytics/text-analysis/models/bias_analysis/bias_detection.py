# models/bias_analysis/bias_detection.py
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

# Download NLTK data files (only needed once)
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_texts(texts):
    stop_words = set(stopwords.words('english'))
    processed_texts = []
    for text in texts:
        tokens = word_tokenize(text)
        tokens = [t.lower() for t in tokens if t.isalpha()]
        tokens = [t for t in tokens if t not in stop_words]
        processed_texts.append(' '.join(tokens))
    return processed_texts

def analyze_bias(texts):
    processed_texts = preprocess_texts(texts)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(processed_texts)
    bias_scores = X.sum(axis=1).A1  # Sum TF-IDF scores as a dummy metric
    return [{'text': text, 'bias_score': score} for text, score in zip(texts, bias_scores)]