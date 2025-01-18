from typing import List, Dict
import logging
from datetime import datetime

class ContentPreprocessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.required_fields = ['summary_text', 'source', 'url']

    def preprocess_summaries(self, summaries: List[Dict]) -> List[Dict]:
        """Preprocess summaries before article generation"""
        try:
            processed_summaries = []
            
            for summary in summaries:
                # Validate required fields
                if not self._validate_summary(summary):
                    self.logger.warning(f"Skipping invalid summary from {summary.get('source', 'unknown')}")
                    continue

                # Process and structure the summary
                processed_summary = {
                    'processed_text': self._clean_text(summary['summary_text']),
                    'source_metadata': {
                        'url': summary['url'],
                        'source': summary['source'],
                        'timestamp': summary.get('timestamp', datetime.now().isoformat())
                    },
                    'analysis_data': {
                        'sentiment': summary.get('sentiment_analysis', {}),
                        'bias': summary.get('bias_analysis', {}),
                        'keywords': summary.get('keywords', [])
                    }
                }
                
                processed_summaries.append(processed_summary)

            if not processed_summaries:
                raise ValueError("No valid summaries to process")
                
            return processed_summaries

        except Exception as e:
            self.logger.error(f"Preprocessing failed: {str(e)}")
            raise

    def _validate_summary(self, summary: Dict) -> bool:
        """Check if summary has all required fields"""
        return all(field in summary and summary[field] for field in self.required_fields)

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
            
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Remove any unwanted characters or patterns
        text = text.replace("...", ".")
        text = text.replace("  ", " ")
        
        return text.strip()