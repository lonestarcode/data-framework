from typing import Dict, List, Any
from bs4 import BeautifulSoup
from .base_text_scraper import BaseTextScraper
from datetime import datetime

class NewsScraper(BaseTextScraper):
    """Scraper for news articles"""
    
    def __init__(self):
        super().__init__(name="news")
        
    async def scrape(self, params: Dict[str, Any]) -> List[Dict]:
        """Scrape news articles based on provided parameters"""
        url = params.get('url')
        if not url:
            self.logger.error("No URL provided")
            return []
            
        try:
            html_content = await self._fetch_url(url)
            if not html_content:
                return []
                
            soup = BeautifulSoup(html_content, 'html.parser')
            articles = []
            
            # Extract articles based on common news site patterns
            for article in soup.find_all(['article', 'div'], class_=['article', 'post']):
                article_data = {
                    'url': url,
                    'timestamp': datetime.utcnow().isoformat(),
                    'title': self._extract_title(article),
                    'content': self._extract_content(article),
                    'author': self._extract_author(article),
                    'published_date': self._extract_date(article)
                }
                articles.append(article_data)
                
            return articles
            
        except Exception as e:
            self.logger.error(f"Error scraping news: {str(e)}")
            return []
            
    def _extract_title(self, article_soup) -> str:
        """Extract article title"""
        title_tag = article_soup.find(['h1', 'h2'])
        return title_tag.get_text().strip() if title_tag else ""
        
    def _extract_content(self, article_soup) -> str:
        """Extract article content"""
        content_tags = article_soup.find_all(['p', 'div'], class_=['content', 'article-body'])
        return " ".join(tag.get_text().strip() for tag in content_tags)
        
    def _extract_author(self, article_soup) -> str:
        """Extract article author"""
        author_tag = article_soup.find(['span', 'a'], class_=['author', 'byline'])
        return author_tag.get_text().strip() if author_tag else ""
        
    def _extract_date(self, article_soup) -> str:
        """Extract article publication date"""
        date_tag = article_soup.find(['time', 'span'], class_=['date', 'published'])
        return date_tag.get('datetime', '') if date_tag else ""
