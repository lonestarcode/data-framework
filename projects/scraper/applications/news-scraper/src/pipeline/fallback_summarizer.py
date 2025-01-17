from typing import Dict
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

class BasicSummarizer:
    def __init__(self):
        nltk.download('punkt')
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))

    def generate_summary(self, text: str, source: str) -> Dict[str, str]:
        # Tokenize the text into sentences
        sentences = sent_tokenize(text)
        
        # Tokenize words and remove stopwords
        words = word_tokenize(text.lower())
        word_tokens = [word for word in words if word.isalnum() and word not in self.stop_words]
        
        # Calculate word frequencies
        freq_dist = FreqDist(word_tokens)
        
        # Score sentences based on word frequencies
        sentence_scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in freq_dist:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = freq_dist[word]
                    else:
                        sentence_scores[sentence] += freq_dist[word]
        
        # Get top 3 sentences for summary
        summary_sentences = sorted(
            sentence_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        summary = ' '.join([s[0] for s in summary_sentences])
        
        return {
            "summary": summary,
            "model": "basic_summarizer"
        }

def handle_fallback(fallback_type: str, *args, **kwargs) -> Dict:
    if fallback_type == "basic_summarizer":
        summarizer = BasicSummarizer()
        return summarizer.generate_summary(*args, **kwargs)
    else:
        raise ValueError(f"Unknown fallback type: {fallback_type}") 