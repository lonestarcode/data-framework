from src.logging.logger import get_logger, log_execution_time

logger = get_logger('scraper')

class BaseScraper:
    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(f'scraper.{name}')
    
    @log_execution_time(logger)
    def scrape(self, url: str):
        self.logger.info(f"Starting scrape for {url}", 
                        extra={"scraper": self.name, "url": url})
        try:
            # Scraping logic here
            pass
        except Exception as e:
            self.logger.error(f"Scraping failed for {url}: {str(e)}", 
                            extra={"scraper": self.name, "url": url},
                            exc_info=True)
            raise
