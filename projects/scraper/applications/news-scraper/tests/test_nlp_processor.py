import pytest
from src.pipeline.nlp_processor import NLPProcessor

class TestNLPProcessor:
    @pytest.fixture
    def processor(self):
        return NLPProcessor()

    def test_extract_keywords(self, processor):
        text = "Artificial intelligence and machine learning are transforming technology"
        keywords = processor.extract_keywords(text, num_keywords=3)
        
        assert len(keywords) <= 3
        assert "artificial intelligence" in [k.lower() for k in keywords]
        assert "machine learning" in [k.lower() for k in keywords]

    def test_filter_irrelevant_content(self, processor):
        news_text = "Breaking: Major technology company announces new AI product"
        spam_text = "Buy now! Amazing discount on products!!!"
        
        assert processor.filter_irrelevant_content(news_text) == True
        assert processor.filter_irrelevant_content(spam_text) == False 