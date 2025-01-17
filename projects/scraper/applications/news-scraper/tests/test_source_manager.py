import pytest
from src.api.source_manager import SourceManager
from datetime import datetime

class TestSourceManager:
    @pytest.fixture
    def manager(self, db_session):
        return SourceManager(db_session)

    def test_add_source(self, manager):
        source_data = {
            "name": "Test News",
            "url": "https://test.com",
            "type": "news",
            "interval": "1h"
        }
        
        result = manager.add_source(source_data)
        assert result["status"] == "success"
        assert "source_id" in result

    def test_get_sources(self, manager):
        # Add test sources
        source_data = [
            {"name": "News1", "url": "https://news1.com", "type": "news"},
            {"name": "Blog1", "url": "https://blog1.com", "type": "blog"}
        ]
        
        for source in source_data:
            manager.add_source(source)
        
        # Test filtering
        news_sources = manager.get_sources(source_type="news")
        assert len(news_sources) == 1
        assert news_sources[0]["name"] == "News1" 