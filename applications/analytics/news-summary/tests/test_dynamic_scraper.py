import pytest
from src.scraper.dynamic_scraper import DynamicScraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestDynamicScraper:
    @pytest.fixture
    def scraper(self):
        return DynamicScraper(name="test_dynamic")

    def test_scrape_dynamic_content(self, scraper, mock_webdriver):
        # Mock Selenium WebDriver behavior
        mock_webdriver.get.return_value = None
        mock_element = mock_webdriver.find_element.return_value
        mock_element.text = "Dynamically loaded content"

        result = scraper.scrape("https://test.com/dynamic")
        assert "Dynamically loaded content" in result["text"]

    def test_scrape_javascript_error(self, scraper, mock_webdriver):
        # Test handling of JavaScript errors
        mock_webdriver.get.side_effect = Exception("JavaScript error")

        with pytest.raises(Exception) as exc_info:
            scraper.scrape("https://test.com/js-error")
        assert "JavaScript error" in str(exc_info.value)

    def test_scrape_timeout(self, scraper, mock_webdriver):
        # Test handling of timeout waiting for dynamic content
        mock_webdriver.find_element.side_effect = TimeoutError()

        with pytest.raises(Exception) as exc_info:
            scraper.scrape("https://test.com/timeout")
        assert "Timeout waiting for content" in str(exc_info.value)
