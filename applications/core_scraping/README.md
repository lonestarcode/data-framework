# Core Scraping

Core scraping module for collecting data from various sources. Provides base functionality and specialized implementations for text and media scraping.

## Structure
- `base/`: Core shared functionality and interfaces
  - `interfaces/`: Base scraping interfaces
  - `utils/`: Common utilities
  - `constants/`: Shared constants
  - `schemas/`: Data structure definitions
  - `errors/`: Error handling
  - `config/`: Configuration management
- `text-scrape/`: Text-specific scraping implementation
- `media-scrape/`: Media-specific scraping implementation
- `cli/`: Command-line interface tools

## Features
- Standardized data collection
- Configurable scraping rules
- Error handling and retry mechanisms
- Data validation and cleaning
- Raw data storage management
- Monitoring and logging

## Usage
Each scraping module (text/media) follows the same interface defined in base, but implements specific logic for its data type. Raw data is saved in standardized format under each module's `data/raw/` directory.