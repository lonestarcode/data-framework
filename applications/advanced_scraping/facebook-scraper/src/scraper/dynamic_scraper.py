from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.logging.logger import get_logger

logger = get_logger(__name__)

class DynamicScraper:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.binary_location = '/usr/bin/chromium'
        
    def __enter__(self):
        self.driver = webdriver.Chrome(options=self.options)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()
            
    async def scrape_category(self, category: str):
        try:
            url = f"https://www.facebook.com/marketplace/category/{category}"
            self.driver.get(url)
            
            # Wait for listings to load
            listings = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "[data-testid='marketplace_listing_item']")
                )
            )
            
            return [self._parse_listing(listing) for listing in listings]
            
        except Exception as e:
            logger.error(f"Error scraping category {category}: {str(e)}")
            raise
            
    def _parse_listing(self, element):
        try:
            return {
                'title': element.find_element(By.CSS_SELECTOR, 'h2').text,
                'price': element.find_element(By.CSS_SELECTOR, '[data-testid="price"]').text,
                'location': element.find_element(By.CSS_SELECTOR, '[data-testid="location"]').text,
                'url': element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            }
        except Exception as e:
            logger.error(f"Error parsing listing: {str(e)}")
            return None
