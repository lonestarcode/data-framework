import pytest
from src.monitoring.metrics import (
    SCRAPE_COUNTER, SCRAPE_FAILURES, SCRAPE_DURATION,
    PROCESSING_ERRORS, SUMMARY_GENERATION_TIME
)

class TestMetrics:
    def test_scrape_counter(self):
        initial_count = SCRAPE_COUNTER._value.get()
        SCRAPE_COUNTER.inc()
        assert SCRAPE_COUNTER._value.get() == initial_count + 1

    def test_scrape_duration(self):
        with SCRAPE_DURATION.time():
            # Simulate work
            pass
        assert SCRAPE_DURATION._sum.get() > 0

    def test_error_counters(self):
        initial_errors = PROCESSING_ERRORS._value.get()
        PROCESSING_ERRORS.inc()
        assert PROCESSING_ERRORS._value.get() == initial_errors + 1 