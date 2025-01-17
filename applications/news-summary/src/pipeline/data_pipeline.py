from src.scraper.base import BaseScraper
from src.pipeline.nlp_processor import NLPProcessor
from src.pipeline.llm_handler import LLMHandler
from src.monitoring.metrics import (
    SCRAPE_COUNTER, SCRAPE_DURATION,
    PROCESSING_ERRORS, SUMMARY_GENERATION_TIME
)
from src.logging.logger import get_logger, log_execution_time
from src.database.models import Article, Summary
from typing import List, Dict
import time
from src.pipeline.error_handler import with_error_handling, ScraperError

logger = get_logger('pipeline')

class DataPipeline:
    def __init__(self, db_session, scraper, nlp_processor, llm_handler):
        self.db = db_session
        self.scraper = scraper
        self.nlp_processor = nlp_processor
        self.llm_handler = llm_handler
        self.logger = get_logger('pipeline')

    @with_error_handling(max_retries=3, base_delay=5)
    def process_source(self, url: str) -> Dict:
        try:
            # Scrape content
            SCRAPE_COUNTER.inc()
            with SCRAPE_DURATION.time():
                content = self.scraper.scrape(url)

            # Filter irrelevant content
            if not self.nlp_processor.filter_irrelevant_content(content['text']):
                self.logger.info(f"Content filtered as irrelevant: {url}")
                return {"status": "filtered", "url": url}

            # Extract keywords
            keywords = self.nlp_processor.extract_keywords(content['text'])

            # Store article with transaction
            with self.db.begin():
                article = Article(
                    title=content['title'],
                    content=content['text'],
                    url=url,
                    source=self.scraper.name,
                    keywords=keywords
                )
                self.db.add(article)
                self.db.flush()

                # Generate summary
                with SUMMARY_GENERATION_TIME.time():
                    summary_data = self.llm_handler.generate_summary(
                        content['text'],
                        source=self.scraper.name
                    )

                # Store summary
                summary = Summary(
                    article_id=article.id,
                    summary_text=summary_data['summary'],
                    model_used=summary_data['model'],
                    keywords=keywords
                )
                self.db.add(summary)

            return {
                "status": "success",
                "article_id": article.id,
                "summary_id": summary.id
            }

        except Exception as e:
            self.logger.error(
                f"Error processing source {url}: {str(e)}",
                exc_info=True
            )
            raise

    @with_error_handling(max_retries=2, base_delay=30)
    def process_batch(self, urls: List[str]) -> List[Dict]:
        results = []
        for url in urls:
            try:
                result = self.process_source(url)
                results.append(result)
            except ScraperError as e:
                self.logger.warning(
                    f"Failed to process {url}: {str(e)}",
                    extra={"error_type": e.error_type}
                )
                results.append({
                    "status": "error",
                    "url": url,
                    "error": str(e)
                })
                continue
        return results
