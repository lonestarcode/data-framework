import pytest
from datetime import datetime
from src.pipeline.generator_pipeline import ContentGeneratorPipeline
from src.models.content import Article

class TestContentGenerator:
    @pytest.fixture
    def generator(self, test_config):
        return ContentGeneratorPipeline(config=test_config)

    @pytest.fixture
    def mock_summaries(self):
        return [
            {
                'summary_text': 'First test summary about AI developments.',
                'source': 'TechNews',
                'url': 'https://technews.com/article1',
                'sentiment_analysis': {'positive': 0.8, 'negative': 0.2},
                'bias_analysis': {'political': 0.1, 'technical': 0.8},
                'keywords': ['AI', 'technology', 'development']
            },
            {
                'summary_text': 'Second test summary about machine learning.',
                'source': 'AIDaily',
                'url': 'https://aidaily.com/article2',
                'sentiment_analysis': {'positive': 0.6, 'negative': 0.4},
                'bias_analysis': {'political': 0.2, 'technical': 0.7},
                'keywords': ['ML', 'AI', 'research']
            }
        ]

    def test_generate_article_success(self, generator, mock_summaries):
        topic = "AI Technology Trends"
        result = generator.generate_article(mock_summaries, topic)
        
        assert isinstance(result, Article)
        assert result.topic == topic
        assert len(result.sources) == 2
        assert result.status == "success"
        assert isinstance(result.generated_at, datetime)
        assert len(result.keywords) > 0
        assert all(k in result.sentiment_scores for k in ['positive', 'negative'])
        assert all(k in result.bias_metrics for k in ['political', 'technical'])

    def test_generate_article_empty_summaries(self, generator):
        with pytest.raises(ValueError) as exc_info:
            generator.generate_article([], "Test Topic")
        assert "No valid summaries to process" in str(exc_info.value)

    def test_aggregate_sentiments(self, generator, mock_summaries):
        sentiments = generator._aggregate_sentiments(mock_summaries)
        assert 'positive' in sentiments
        assert 'negative' in sentiments
        assert abs(sentiments['positive'] - 0.7) < 0.01  # Average of 0.8 and 0.6

    def test_extract_common_keywords(self, generator, mock_summaries):
        keywords = generator._extract_common_keywords(mock_summaries)
        assert 'AI' in keywords  # Should be present in both summaries
        assert len(keywords) <= 5  # As specified in the implementation

    @pytest.mark.integration
    def test_end_to_end_generation(self, generator, mock_summaries):
        topic = "AI Technology Trends"
        result = generator.generate_article(mock_summaries, topic)
        
        # Check content quality
        assert len(result.content.split()) >= 100  # Minimum word count
        assert topic.lower() in result.content.lower()  # Topic is mentioned
        assert all(url in str(result.sources) for url in 
                  ['technews.com', 'aidaily.com'])  # Sources are included