# Scrape-Text

A robust text scraping framework designed to collect and clean textual data from multiple sources. Part of the larger data science framework's data collection pipeline.

## 🎯 Purpose

Scrape-Text serves as the data collection layer, focusing on:
- Multi-source text extraction (news, social media, documents)
- Initial text cleaning and validation
- Structured data storage
- Rate-limited and proxy-supported scraping

## 🏗 Architecture

```
scrape-text/
├── src/
│   ├── scrapers/                 # Source-specific scrapers
│   │   ├── news_scraper.py      # News website scraping
│   │   ├── social_scraper.py    # Social media content
│   │   ├── document_scraper.py  # Document processing
│   │   └── api_collectors/      # API-based collectors
│   │       ├── twitter_api.py
│   │       └── reddit_api.py
│   ├── processors/              # Basic processing
│   │   ├── html_cleaner.py     # HTML removal
│   │   ├── text_validator.py   # Content validation
│   │   └── metadata_extractor.py # Extract article metadata
│   └── utils/                  # Shared utilities
│       ├── rate_limiter.py     # API rate limiting
│       ├── proxy_manager.py    # Proxy rotation
│       └── url_validator.py    # URL validation
├── data/
│   ├── raw/                   # Original scraped content
│   └── processed/             # Cleaned text
├── config/
│   ├── scraper_config.yaml   # Scraping rules
│   └── api_config.yaml       # API credentials
└── tests/
    ├── unit/
    └── integration/
```

## 🚀 Features

### 1. News Scraping
```python
response = news_scraper.scrape('https://example.com/news')
# Returns: {'url': '...', 'title': '...', 'content': '...', 'metadata': {...}}
```

### 2. Social Media Collection
```python
tweets = twitter_collector.collect('#AI', max_results=100)
# Returns: [{'id': '...', 'text': '...', 'user': '...', 'timestamp': '...'}, ...]
```

### 3. Document Processing
```python
content = document_scraper.process('document.pdf')
# Returns: {'content': '...', 'pages': 5, 'metadata': {...}}
```

## 📋 Requirements

```bash
pip install -r requirements.txt
```

Key dependencies:
- beautifulsoup4==4.12.2
- requests==2.31.0
- aiohttp==3.8.5
- tweepy==4.14.0
- pdfminer.six==20221105
- python-dotenv==1.0.0

## ⚙️ Configuration

### Scraper Configuration
```yaml
# config/scraper_config.yaml
news_sources:
  - name: "Tech News"
    url: "https://technews.com"
    selectors:
      article: "article.news-item"
      title: "h1.title"
      content: "div.content"
      date: "span.date"
    rate_limit: 1  # requests per second

social_sources:
  - platform: "twitter"
    search_terms:
      - "#technology"
      - "#AI"
    max_results: 100
    interval: 3600  # seconds between searches
```

## 🏃‍♂️ Usage

### Run Scraping Pipeline
```bash
# Run all scrapers
python scripts/run_scrapers.py

# Run specific scraper
python scripts/run_scrapers.py --source news
```

### Monitor Progress
```bash
# View scraping status
python scripts/check_status.py

# View error logs
python scripts/view_logs.py
```

## 🔄 Integration Points

### Output Format
```json
{
    "id": "unique_id",
    "url": "source_url",
    "title": "article_title",
    "content": "cleaned_content",
    "metadata": {
        "author": "author_name",
        "date": "2023-10-20T10:00:00Z",
        "category": "technology"
    },
    "scrape_timestamp": "2023-10-20T10:05:00Z"
}
```

### Next Steps
- Data flows to analysis-text for:
  - Summarization
  - Sentiment analysis
  - Topic modeling
  - Bias detection

## 📊 Monitoring

### Health Checks
```bash
# Check scraper health
python monitoring/health_check.py

# View scraping metrics
python monitoring/view_metrics.py
```

### Key Metrics
- Scraping success rate
- Content validation rate
- API rate limit status
- Proxy rotation status

## 🧪 Testing

```bash
# Run all tests
pytest

# Test specific scraper
pytest tests/unit/test_news_scraper.py
```

## 🔒 Security

- API keys stored in environment variables
- Proxy support for anonymity
- Rate limiting for API compliance
- URL and content validation
- Error handling and logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.