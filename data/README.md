This directory manages the centralized data storage for ML training and cross-project analytics, implementing the data workflow described in the architecture documentation.

## Directory Structure

```
data/
├── raw/                      # Raw data from all sources
│   ├── text/                # Raw text data (articles, social media)
│   ├── market/             # Raw market data (prices, trades)
│   └── media/              # Raw media data (images, videos)
├── processed/               # Cleaned and normalized data
│   ├── mongodb/            # Processed but unstructured data
│   └── sql/                # Structured and validated data
└── validated/              # Production-ready datasets
    ├── training/          # Training datasets
    ├── testing/           # Testing datasets
    └── production/        # Production datasets
```

## Data Flow

1. **Raw Data Collection**
   - Applications store data in their local databases
   - Data is copied to the global database for ML/analytics
   - Supports various data types (text, market data, social content)

2. **Data Processing**
   - Raw data is processed and standardized
   - Features are extracted for ML training
   - Validation ensures data quality

3. **Data Access**
   - ML models access training data
   - Analytics services query processed data
   - Applications receive model predictions

## Database Integration

### MongoDB Collections
- Raw training data storage
- Unstructured content (text, social media)
- Real-time data streams
- Model predictions and embeddings

### SQL Tables
- Validated market metrics
- User interactions
- Performance statistics
- Model evaluation results

## Key Components

1. **Data Models** (`models/`)
   - Base data structures
   - Validation schemas
   - Type definitions

2. **Database Managers** (`database/`)
   - MongoDB operations
   - SQL operations
   - Data synchronization

3. **Utilities** (`utils/`)
   - Data validation
   - Preprocessing functions
   - Common helpers

## Usage Example

```python
from data.manager import GlobalDataManager

# Initialize manager
data_manager = GlobalDataManager(mongo_uri, sql_uri)

# Store raw data
data_id = await data_manager.store_raw_data(
    source="facebook_marketplace",
    data_type="listing",
    content=listing_data
)

# Get data for processing
raw_data = await data_manager.get_data_for_processing("listing")
```

## Data Types

1. **Text Data**
   - News articles
   - Social media content
   - Market analysis

2. **Market Data**
   - Real-time prices
   - Trading volumes
   - Market indicators

3. **User Interaction Data**
   - Feedback
   - Usage patterns
   - Performance metrics

## Contributing

1. Follow the data validation guidelines
2. Use appropriate database for data type
3. Maintain bidirectional data flow
4. Document any schema changes
```

This README follows the data management patterns described in:
```
startLine: 303
endLine: 318
```

And implements the database strategy outlined in:
```
startLine: 515
endLine: 532
```

The bidirectional data flow is based on:
```
startLine: 505
endLine: 511
```
