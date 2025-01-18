# Core Analytics

Core analytics module for processing and analyzing scraped data. Handles both text and media analytics with specialized processing pipelines.

## Structure
- `base/`: Core shared functionality
  - `pipeline/`: Data processing pipelines
  - `models/`: Analytics models
  - `enrichment/`: Data enrichment tools
  - `validation/`: Data validation
  - `output/`: Output formatting and export
- `text-analytics/`: Text-specific analysis
- `media-analytics/`: Media-specific analysis

## Features
- Data cleaning and preprocessing
- Advanced analytics pipelines
- Machine learning model integration
- Quality control and validation
- Standardized output formats
- Performance monitoring
- Result storage and export

## Usage
Analytics modules process data from the raw directory, apply necessary transformations and analysis, and store results in the processed directory for use by automated workflows.