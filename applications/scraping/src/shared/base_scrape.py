from typing import Dict, List, Any
from datetime import datetime
import logging
from .interfaces.scraper_interface import ScraperInterface

class BaseScraper(ScraperInterface):
    """Base implementation of the scraper interface"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"scraper.{name}")
        
    async def scrape(self, params: Dict[str, Any]) -> List[Dict]:
        """Base scraping method to be implemented by child classes"""
        raise NotImplementedError
        
    async def validate(self, data: List[Dict]) -> List[Dict]:
        """Basic validation of scraped data"""
        return [item for item in data if self._is_valid_item(item)]
        
    async def clean(self, data: List[Dict]) -> List[Dict]:
        """Basic cleaning of scraped data"""
        return [self._clean_item(item) for item in data]
        
    async def store(self, data: List[Dict]) -> bool:
        """Store data with timestamp"""
        try:
            timestamp = datetime.utcnow()
            for item in data:
                item['scraped_at'] = timestamp
            return await self._save_to_storage(data)
        except Exception as e:
            self.logger.error(f"Storage error: {str(e)}")
            return False
            
    def _is_valid_item(self, item: Dict) -> bool:
        """Override in child classes for specific validation"""
        return bool(item)
        
    def _clean_item(self, item: Dict) -> Dict:
        """Override in child classes for specific cleaning"""
        return item
        
    async def _save_to_storage(self, data: List[Dict]) -> bool:
        """Override in child classes for specific storage implementation"""
        raise NotImplementedError