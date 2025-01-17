# models/language_detection/language_model.py
from langdetect import detect

def detect_language(texts):
    results = []
    for text in texts:
        try:
            lang = detect(text)
            results.append({'text': text, 'language': lang})
        except:
            results.append({'text': text, 'language': 'unknown'})
    return results