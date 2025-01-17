from apscheduler.schedulers.background import BackgroundScheduler
from src.scraper.base import BaseScraper
from src.database.models import Source
from src.logging.logger import get_logger

logger = get_logger('scheduler')

class ScraperScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scrapers = {}

    def init_scrapers(self):
        sources = Source.query.all()
        for source in sources:
            self.add_source(source)

    def add_source(self, source):
        scraper = BaseScraper(source.name)
        self.scrapers[source.id] = scraper
        
        # Add job based on interval
        self.scheduler.add_job(
            scraper.scrape,
            'interval',
            hours=int(source.interval.replace('h', '')),
            args=[source.url]
        )

    def start(self):
        self.init_scrapers()
        self.scheduler.start()
        logger.info("Scraper scheduler started") 