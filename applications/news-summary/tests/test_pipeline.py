import pytest
from src.pipeline.data_pipeline import DataPipeline
from src.database.models import Article, Summary
from datetime import datetime

class TestDataPipeline:
    @pytest.fixture
    def pipeline(self, db_session, mock_scraper, mock_nlp_processor, mock_llm_handler):
        return DataPipeline(
            db_session=db_session,
            scraper=mock_scraper,
            nlp_processor=mock_nlp_processor,
            llm_handler=mock_llm_handler
        )

    def test_process_source_success(self, pipeline, db_session):
        # Test successful processing of a source
        result = pipeline.process_source("https://test.com/article")
        
        assert result["status"] == "success"
        assert "article_id" in result
        assert "summary_id" in result
        
        # Verify database entries
        article = db_session.query(Article).first()
        assert article is not None
        assert article.url == "https://test.com/article"
        
        summary = db_session.query(Summary).first()
        assert summary is not None
        assert summary.article_id == article.id

    def test_process_source_irrelevant_content(self, pipeline, mock_nlp_processor):
        # Configure NLP processor to mark content as irrelevant
        mock_nlp_processor.filter_irrelevant_content.return_value = False
        
        result = pipeline.process_source("https://test.com/spam")
        assert result["status"] == "filtered"

    def test_process_source_scraping_error(self, pipeline, mock_scraper):
        # Simulate scraping error
        mock_scraper.scrape.side_effect = Exception("Network error")
        
        with pytest.raises(Exception) as exc_info:
            pipeline.process_source("https://test.com/error")
        assert "Network error" in str(exc_info.value)

    def test_process_source_summary_generation_error(self, pipeline, mock_llm_handler):
        # Simulate LLM error
        mock_llm_handler.generate_summary.side_effect = Exception("API error")
        
        with pytest.raises(Exception) as exc_info:
            pipeline.process_source("https://test.com/article")
        assert "API error" in str(exc_info.value)
