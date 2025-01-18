from src.scraper.dynamic_scraper import DynamicScraper
from src.scraper.api_scraper import APIScraper
from src.scraper.static_scraper import StaticScraper
from src.scraper.llm_scraper import LLMScraper
from src.logging.logger import get_logger

logger = get_logger(__name__)

class ScraperFactory:
    @staticmethod
    def get_scraper(scraper_type: str):
        scrapers = {
            'dynamic': DynamicScraper,
            'api': APIScraper,
            'static': StaticScraper,
            'llm': LLMScraper
        }
        
        if scraper_type not in scrapers:
            logger.error(f"Invalid scraper type: {scraper_type}")
            raise ValueError(f"Invalid scraper type: {scraper_type}")
            
        return scrapers[scraper_type]()