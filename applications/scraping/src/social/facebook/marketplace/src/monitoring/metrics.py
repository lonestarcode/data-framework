from prometheus_client import Counter, Histogram

# Scraping metrics
SCRAPE_COUNTER = Counter(
    'marketplace_scrape_total',
    'Total number of marketplace scraping operations',
    ['category', 'scraper_type']
)

SCRAPE_DURATION = Histogram(
    'marketplace_scrape_duration_seconds',
    'Time spent scraping marketplace listings',
    ['category', 'scraper_type']
)

# Processing metrics
PROCESSING_ERRORS = Counter(
    'marketplace_processing_errors_total',
    'Total number of processing errors',
    ['error_type']
)

# LLM metrics
SUMMARY_GENERATION_TIME = Histogram(
    'marketplace_llm_summary_duration_seconds',
    'Time spent generating summaries with LLM',
    ['model']
)
