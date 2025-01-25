from typing import Dict, List, Any
from core_scraping.base.base_scrape import BaseScraper
import aiohttp
import logging

class BaseTextScraper(BaseScraper):
    """Base class for all text-based scrapers"""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.session = None
        
    async def __aenter__(self):
        """Setup async context with HTTP session"""
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup async context"""
        if self.session:
            await self.session.close()
            
    async def _fetch_url(self, url: str, headers: Dict = None) -> str:
        """Fetch content from URL with error handling"""
        try:
            async with self.session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.text()
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {str(e)}")
            return ""
            
    def _clean_text(self, text: str) -> str:
        """Common text cleaning operations"""
        if not text:
            return ""
        # Remove extra whitespace
        text = " ".join(text.split())
        # Remove special characters if needed
        # Normalize unicode if needed
        return text.strip()
        
    async def _extract_text_content(self, html_content: str, selectors: List[str]) -> str:
        """Extract text content using CSS selectors"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            text_parts = []
            for selector in selectors:
                elements = soup.select(selector)
                text_parts.extend([elem.get_text() for elem in elements])
            return "\n".join(text_parts)
        except Exception as e:
            self.logger.error(f"Error extracting text content: {str(e)}")
            return ""
            
    def _is_valid_text(self, text: str, min_length: int = 10) -> bool:
        """Validate text content"""
        if not text or len(text.strip()) < min_length:
            return False
        # Add more text validation as needed
        return True