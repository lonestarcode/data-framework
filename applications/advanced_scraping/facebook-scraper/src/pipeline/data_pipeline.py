from src.scraper.factory import ScraperFactory
from src.monitoring.metrics import SCRAPE_COUNTER, SCRAPE_DURATION
from src.logging.logger import get_logger
from src.database.models import MarketplaceListing, ListingAnalysis
from src.pipeline.error_handler import with_error_handling
from src.database.session import get_db_session

logger = get_logger('pipeline')

class MarketplacePipeline:
    def __init__(self):
        self.dynamic_scraper = ScraperFactory.get_scraper('dynamic')
        self.api_scraper = ScraperFactory.get_scraper('api')
        self.llm_scraper = ScraperFactory.get_scraper('llm')
    
    @with_error_handling
    async def process_category(self, category: str):
        try:
            # Get raw listings
            raw_listings = await self.dynamic_scraper.scrape_category(category)
            
            # Enrich with API data
            enriched_listings = await self.api_scraper.enrich_listings(raw_listings)
            
            # Process with LLM
            processed_listings = await self.llm_scraper.process_listings(
                enriched_listings
            )
            
            # Store results
            await self._store_listings(processed_listings)
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise

    async def _store_listings(self, listings):
        """Store processed listings in the database"""
        async for session in get_db_session():
            try:
                for listing_data in listings:
                    # Create marketplace listing
                    listing = MarketplaceListing(
                        listing_id=listing_data['url'].split('/')[-1],
                        title=listing_data['title'],
                        price=float(listing_data['price'].replace('$', '')),
                        location=listing_data['location'],
                        listing_url=listing_data['url'],
                        category=listing_data.get('category', 'unknown'),
                        description=listing_data.get('description', ''),
                        seller_id=listing_data.get('seller_id'),
                        images=listing_data.get('images', [])
                    )
                    session.add(listing)
                    await session.flush()

                    # Create listing analysis
                    if 'analysis' in listing_data:
                        analysis = ListingAnalysis(
                            listing_id=listing.id,
                            quality_score=listing_data['analysis'].get('confidence', 0.0),
                            keywords=listing_data['analysis'].get('keywords', []),
                            category_confidence=listing_data['analysis'].get('category_confidence', 0.0)
                        )
                        session.add(analysis)

                await session.commit()
                
            except Exception as e:
                await session.rollback()
                self.logger.error(f"Error storing listings: {str(e)}")
                raise