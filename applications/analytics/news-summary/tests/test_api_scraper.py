import pytest
from src.scraper.api_scraper import APIScraper
import requests
from unittest.mock import Mock

class TestAPIScraper:
    @pytest.fixture
    def scraper(self):
        return APIScraper(
            name="test_api",
            base_url="https://api.test.com",
            api_key="test_key"
        )

    def test_scrape_success(self, scraper, requests_mock):
        # Mock successful API response
        mock_data = {
            "title": "Test Article",
            "content": "Test content",
            "published_at": "2024-03-15T12:00:00Z"
        }
        requests_mock.get(
            "https://api.test.com/articles",
            json=mock_data
        )

        result = scraper.scrape("test_endpoint")
        assert result["title"] == "Test Article"
        assert result["text"] == "Test content"

    def test_scrape_rate_limit(self, scraper, requests_mock):
        # Test rate limiting handling
        requests_mock.get(
            "https://api.test.com/articles",
            status_code=429
        )

        with pytest.raises(Exception) as exc_info:
            scraper.scrape("test_endpoint")
        assert "Rate limit exceeded" in str(exc_info.value)

    def test_scrape_auth_error(self, scraper, requests_mock):
        # Test authentication error
        requests_mock.get(
            "https://api.test.com/articles",
            status_code=401
        )

        with pytest.raises(Exception) as exc_info:
            scraper.scrape("test_endpoint")
        assert "Authentication failed" in str(exc_info.value)
