# Facebook Marketplace Scraper

A robust and modular scraper designed to collect and display the newest listings from Facebook Marketplace in specific categories (e.g., bikes). This project provides a solution for accessing and viewing public listings efficiently, even after Facebook has removed the "sort by newest" feature.

## Features

- **Multi-Strategy Scraping**:
  - Dynamic scraping for JavaScript-rendered pages (Selenium/Playwright).
  - API integration using Facebook GraphQL (if accessible).
  - Static scraping for basic HTTP-based pages.

- **Frontend UI**:
  - Displays the newest listings in a user-friendly format.
  - Includes search, filters, and sorting capabilities.

- **Data Processing**:
  - Automated pipelines for cleaning, processing, and enriching scraped data.
  - Optional LLM integration for advanced listing analysis and categorization.

- **Monitoring & Logging**:
  - Prometheus metrics for scraping performance.
  - Robust logging system for error tracking and debugging.

## Installation

### Prerequisites

- **Backend Requirements**:
  - Python 3.9+
  - Docker and Docker Compose (optional but recommended)

- **Frontend Requirements**:
  - Node.js 16+ and npm

- **Browser Drivers** (for dynamic scraping):
  - Chrome/Chromium or Firefox with Selenium WebDriver.

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/facebook-marketplace-scraper.git
   cd facebook-marketplace-scraper

	2.	Backend Setup:
	•	Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


	•	Install dependencies:

pip install -r requirements.txt


	•	Configure scraper settings:
	•	Copy config/scraper_config.yaml.example to config/scraper_config.yaml.
	•	Update the settings for category, location, and scraping intervals.

	3.	Frontend Setup:
	•	Navigate to the frontend directory:

cd frontend
npm install


	•	Start the development server:

npm start


	4.	Start the Backend:
	•	Run the scraper:

python src/main.py


	•	Or start with Docker:

docker-compose up -d



Configuration

Scraper Settings (config/scraper_config.yaml)
	•	Category: Specify the type of listings to scrape (e.g., “bikes”).
	•	Location: Set the geographic location for the search.
	•	Scraping Frequency: Adjust the interval for fetching new listings.

LLM Settings (config/llm_config.yaml)
	•	Integrate AI models for advanced analysis of listings (e.g., categorization, keyword extraction).

Monitoring Settings (config/monitoring_config.yaml)
	•	Configure Prometheus/Grafana for performance tracking.

Usage

Access the UI
	•	Open the frontend at http://localhost:3000 to view the newest listings.

Monitoring Metrics
	•	Access Prometheus: http://localhost:9090
	•	Access Grafana: http://localhost:3000/grafana

Running Tests
	•	Run the test suite with pytest:

pytest tests/



Project Structure

facebook-scraper/
├── config/                 # Configuration files
├── src/                   # Source code
│   ├── scraper/          # Scraping modules
│   ├── pipeline/         # Data processing
│   ├── database/         # Database models
│   ├── api/              # API endpoints
│   └── monitoring/       # Metrics and monitoring
├── tests/                # Test suite
├── frontend/             # Web interface
└── scripts/              # Utility scripts

Known Limitations
	•	Scraping Restrictions:
	•	Dynamic scraping may face challenges like CAPTCHA or IP bans. Use proxies or adjust scraping intervals as needed.
	•	Facebook API:
	•	May require developer credentials and token configuration, and might have restricted access to certain data.

Future Enhancements
	•	Add support for more categories.
	•	Implement notifications for new listings.
	•	Optimize dynamic scraping with headless browsers.

Contributing
	1.	Fork the repository.
	2.	Create a feature branch (git checkout -b feature-name).
	3.	Commit your changes (git commit -m 'Add feature').
	4.	Push to the branch (git push origin feature-name).
	5.	Create a Pull Request.

