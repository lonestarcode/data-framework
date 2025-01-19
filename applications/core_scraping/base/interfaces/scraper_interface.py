from abc import ABC, abstractmethod
from typing import Dict, List, Any

class ScraperInterface(ABC):
    """Base interface for all scrapers in the framework"""
    
    @abstractmethod
    async def scrape(self, params: Dict[str, Any]) -> List[Dict]:
        """Execute the scraping operation"""
        pass
        
    @abstractmethod
    async def validate(self, data: List[Dict]) -> List[Dict]:
        """Validate scraped data"""
        pass
        
    @abstractmethod
    async def clean(self, data: List[Dict]) -> List[Dict]:
        """Clean and normalize scraped data"""
        pass
        
    @abstractmethod
    async def store(self, data: List[Dict]) -> bool:
        """Store the processed data"""
        pass
