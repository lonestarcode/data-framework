import pytest
from src.scraper.static_scraper import StaticScraper
from bs4 import BeautifulSoup

class TestStaticScraper:
    @pytest.fixture
    def scraper(self):
        return StaticScraper(name="test_static")

    def test_scrape_article(self, scraper, requests_mock):
        # Mock HTML content
        html_content = """
        <html>
            <head><title>Test Article</title></head>
            <body>
                <article>
                    <h1>Test Article</h1>
                    <div class="content">Test content</div>
                </article>
            </body>
        </html>
        """
        requests_mock.get("https://test.com/article", text=html_content)

        result = scraper.scrape("https://test.com/article")
        assert result["title"] == "Test Article"
        assert "Test content" in result["text"]

    def test_scrape_invalid_html(self, scraper, requests_mock):
        # Test handling of invalid HTML
        requests_mock.get("https://test.com/invalid", text="Invalid HTML")

        with pytest.raises(Exception) as exc_info:
            scraper.scrape("https://test.com/invalid")
        assert "Failed to parse HTML" in str(exc_info.value)

    def test_scrape_missing_content(self, scraper, requests_mock):
        # Test handling of missing article content
        html_content = "<html><body></body></html>"
        requests_mock.get("https://test.com/empty", text=html_content)

        with pytest.raises(Exception) as exc_info:
            scraper.scrape("https://test.com/empty")
        assert "No article content found" in str(exc_info.value)
