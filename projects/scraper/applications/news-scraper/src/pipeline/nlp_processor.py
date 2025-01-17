from transformers import pipeline
from src.logging.logger import get_logger
import spacy
from typing import List, Dict

logger = get_logger('nlp')

class NLPProcessor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.classifier = pipeline('text-classification')

    def filter_irrelevant_content(self, text: str) -> bool:
        # Use classifier to determine relevance
        result = self.classifier(text)[0]
        return result['label'] == 'RELEVANT' and result['score'] > 0.7

    def extract_keywords(self, text: str, num_keywords: int = 5) -> List[str]:
        doc = self.nlp(text)
        keywords = []
        for chunk in doc.noun_chunks:
            if len(keywords) < num_keywords:
                keywords.append(chunk.text)
        return keywords 