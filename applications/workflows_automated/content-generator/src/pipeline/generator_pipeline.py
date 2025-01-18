from typing import Dict, List
import openai
from datetime import datetime
from src.models.content import Article, GenerationMetrics
from src.pipeline.preprocessor import ContentPreprocessor
from applications.shared.llm.handler import LLMHandler
import logging

class ContentGeneratorPipeline:
    def __init__(self, config: Dict):
        self.config = config
        self.preprocessor = ContentPreprocessor()
        self.llm_handler = LLMHandler(config['llm'])
        self.logger = logging.getLogger(__name__)

    def generate_article(self, summaries: List[Dict], topic: str) -> Article:
        try:
            # Preprocess and validate summaries
            processed_data = self.preprocessor.preprocess_summaries(summaries)
            
            # Combine summaries with their analysis data
            context = self._prepare_generation_context(processed_data, topic)
            
            # Generate article using LLM
            article_content = self.llm_handler.generate_content(
                context=context,
                style_guide=self.config['style_guide']
            )
            
            # Create article with metadata
            return Article(
                topic=topic,
                content=article_content['content'],
                sources=[s['source_metadata']['url'] for s in processed_data],
                generated_at=datetime.now(),
                sentiment_scores=self._aggregate_sentiments(processed_data),
                keywords=self._extract_common_keywords(processed_data),
                bias_metrics=self._calculate_bias_metrics(processed_data),
                model_used=article_content['model']
            )
            
        except Exception as e:
            self.logger.error(f"Article generation failed: {str(e)}")
            raise

    def _prepare_generation_context(self, processed_data: List[Dict], topic: str) -> Dict:
        return {
            "topic": topic,
            "summaries": [d['processed_text'] for d in processed_data],
            "key_points": [d['key_sentences'] for d in processed_data],
            "sentiment_context": [d.get('sentiment_analysis', {}) for d in processed_data],
            "source_context": [d['source_metadata'] for d in processed_data]
        }

    def _aggregate_sentiments(self, data: List[Dict]) -> Dict[str, float]:
        # Aggregate sentiment scores from all sources
        sentiments = {}
        for item in data:
            if 'sentiment_analysis' in item:
                for metric, score in item['sentiment_analysis'].items():
                    sentiments[metric] = sentiments.get(metric, 0) + score
        return {k: v/len(data) for k, v in sentiments.items()}

    def _extract_common_keywords(self, data: List[Dict]) -> List[str]:
        # Extract common keywords across all sources
        keyword_freq = {}
        for item in data:
            for keyword in item.get('keywords', []):
                keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1
        return sorted(keyword_freq, key=keyword_freq.get, reverse=True)[:5]

    def _calculate_bias_metrics(self, data: List[Dict]) -> Dict[str, float]:
        # Calculate aggregate bias metrics
        bias_metrics = {}
        for item in data:
            if 'bias_analysis' in item:
                for metric, score in item['bias_analysis'].items():
                    bias_metrics[metric] = bias_metrics.get(metric, 0) + score
        return {k: v/len(data) for k, v in bias_metrics.items()}