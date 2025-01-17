from prometheus_client import Counter, Histogram, start_http_server
import time

# Scraping metrics
SCRAPE_COUNTER = Counter('scrapes_total', 'Total number of scrape attempts')
SCRAPE_FAILURES = Counter('scrape_failures_total', 'Number of failed scrapes')
SCRAPE_DURATION = Histogram('scrape_duration_seconds', 'Time spent scraping')

# Processing metrics
PROCESSING_ERRORS = Counter('processing_errors_total', 'Number of processing errors')
SUMMARY_GENERATION_TIME = Histogram('summary_generation_seconds', 'Time to generate summaries')

# User feedback metrics
DOWNVOTES = Counter('user_downvotes_total', 'Number of user downvotes')
FEEDBACK_CATEGORIES = Counter('feedback_categories_total', 'Feedback by category') 