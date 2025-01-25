# Text-Scrape

Advanced text scraping module with configurable filters, processing pipelines, and robust error handling.

## 🏗 Directory Structure

```
text-scrape/
├── config/                      # Configuration files
│   ├── filters/                # Filter configurations
│   ├── monitoring/             # Dashboard settings
│   ├── scraper/               # Scraper settings
│   └── storage/               # Storage rules
├── data/                       # Data storage
│   ├── cache/                 # Temporary data
│   ├── processed/             # Processed text
│   └── raw/                   # Raw scraped data
└── src/                        # Source code
    ├── scrapers/              # Data collection
    │   ├── base_text_scraper.py  # Base text scraping functionality
    │   ├── document_scraper.py   # Document format scraping
    │   ├── news_scraper.py       # News content scraping
    │   └── social_scraper.py     # Social media scraping
    ├── cache/                 # Cache management
    ├── dashboard/             # Monitoring interface
    ├── error_handlers/        # Error management
    ├── filters/               # Content filtering
    │   ├── advisory/         # Non-blocking filters
    │   └── prohibitive/      # Blocking filters
    ├── logging/              # Logging system
    ├── migrations/           # Database migrations
    ├── processors/           # Text processing
    ├── proxy_management/     # Proxy handling
    ├── rate_limiters/        # Request throttling
    ├── schemas/              # Data validation
    ├── storage_rules/        # Storage management
    └── validators/           # Input validation
```

## 🚀 Features

### Data Collection
- **Document Scraping**: 
  - Supports PDF, DOCX, and TXT formats
  - Metadata extraction
  - Content parsing with error handling
- **News Scraping**: 
  - Article extraction
  - Title, content, and author parsing
  - Publication date detection
- **Social Media Scraping**:
  - Support for Twitter, LinkedIn, and Facebook
  - API-based content retrieval
  - Platform-specific data parsing

### Base Functionality
- **BaseTextScraper**:
  - Async HTTP session management
  - Common text cleaning utilities
  - HTML content extraction
  - Text validation methods

### Content Filtering
- **Advisory Filters**
  - Reliability assessment
  - Sentiment analysis
- **Prohibitive Filters**
  - Content validation
  - Quality checks

### Processing & Storage
- Text and metadata processing
- Configurable storage rules
- Cache management
- Database migrations

### Safety & Performance
- Rate limiting strategies
- Proxy management
- Error handling
- Input validation

### Monitoring
- Real-time dashboard
- Performance metrics
- Status monitoring
- Logging system

## 🛠 Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure settings:
- Update `config/scraper/config.yaml` for scraper settings
- Adjust `config/filters/filter_rules.yaml` for content filtering
- Modify `config/storage/storage_rules.yaml` for storage rules

3. Initialize database:
```bash
alembic upgrade head
```

## 🔄 Usage

### Basic Scraping Example
```python
from src.scrapers.document_scraper import DocumentScraper
from src.scrapers.news_scraper import NewsScraper
from src.scrapers.social_scraper import SocialScraper

# Document scraping
async with DocumentScraper() as doc_scraper:
    docs = await doc_scraper.scrape({
        'url': 'https://example.com/document.pdf',
        'format': 'pdf'
    })

# News scraping
async with NewsScraper() as news_scraper:
    articles = await news_scraper.scrape({
        'url': 'https://news-site.com/article'
    })

# Social media scraping
async with SocialScraper() as social_scraper:
    posts = await social_scraper.scrape({
        'platform': 'twitter',
        'query': 'search term'
    })
```

## 📊 Data Flow

1. **Collection**: Scrapers gather raw text data
2. **Validation**: Input validators check data integrity
3. **Filtering**: Content passes through advisory and prohibitive filters
4. **Processing**: Text and metadata processors clean and structure data
5. **Storage**: Processed data is stored according to configured rules

## ⚙️ Configuration

- `filter_rules.yaml`: Define content filtering rules
- `config.yaml`: Configure scraper behavior
- `storage_rules.yaml`: Set data storage policies
- `dashboard.yaml`: Configure monitoring settings

## 🔒 Safety Features

- Rate limiting prevents overloading sources
- Proxy management for distributed access
- Error handling for resilient operation
- Input validation for data integrity

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request



