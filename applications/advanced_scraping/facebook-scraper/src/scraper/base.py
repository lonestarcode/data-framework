from src.logging.logger import get_logger, log_execution_time

class BaseScraper:
    """Base class for all Facebook Marketplace scrapers"""
    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(f'scraper.{name}')
        self.base_url = "https://www.facebook.com/marketplace"
    
    @log_execution_time
    def scrape(self, params: dict):
        """Base scraping method to be implemented by child classes"""
        raise NotImplementedError
