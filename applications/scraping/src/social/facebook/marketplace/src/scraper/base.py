from src.core.base_scraper import CoreBaseScraper
from src.logging.logger import log_execution_time

class BaseScraper(CoreBaseScraper):
    """Facebook Marketplace specific base scraper"""
    def __init__(self, name: str):
        super().__init__(name=name)
        self.base_url = "https://www.facebook.com/marketplace"
    
    @log_execution_time
    async def scrape(self, params: dict):
        """Base scraping method to be implemented by child classes"""
        raise NotImplementedError
        
    async def validate(self, data: List[Dict]) -> List[Dict]:
        """Validate Facebook Marketplace data"""
        return [item for item in data if self._is_valid_listing(item)]
        
    async def clean(self, data: List[Dict]) -> List[Dict]:
        """Clean Facebook Marketplace data"""
        return [self._clean_listing(item) for item in data]
        
    def _is_valid_listing(self, listing: Dict) -> bool:
        required_fields = ['title', 'price', 'url']
        return all(field in listing for field in required_fields)
        
    def _clean_listing(self, listing: Dict) -> Dict:
        if 'price' in listing:
            listing['price'] = self._clean_price(listing['price'])
        return listing
        
    def _clean_price(self, price: str) -> float:
        try:
            return float(price.replace('$', '').replace(',', ''))
        except (ValueError, AttributeError):
            return 0.0