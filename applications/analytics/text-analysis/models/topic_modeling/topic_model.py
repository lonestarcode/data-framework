# models/topic_modeling/topic_model.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def analyze_topics(texts, n_topics=3):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    lda = LatentDirichletAllocation(n_components=n_topics)
    lda.fit(X)
    topics = lda.transform(X)
    return [{'text': text, 'topic': topic.argmax()} for text, topic in zip(texts, topics)]