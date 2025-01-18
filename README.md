# Data Science Framework

A comprehensive data science platform featuring advanced scraping, machine learning, and automated workflow capabilities. This framework provides a production-ready foundation for building and deploying data-driven applications.

## 🚀 Core Features




## Data Workflow

### **1. Scraping**
- Scraping applications collect raw data from various sources (e.g., news websites, social media platforms, real estate platforms).
- Data is saved in a standardized format under the `raw/` directory for each application.

### **2. Analytics**
- Analytics applications process, clean, and analyze raw data collected by scrapers.
- The processed data is stored under the `processed/` directory, ready for advanced modeling or analysis.

### **3. Automated Workflows**
- Workflow applications, like the `content-generator`, use processed data to create actionable outputs (e.g., articles, reports, or trading decisions).

---




Applications will have their own local databases, but the data will also be stored in a global database for ML and analytics.

1. **Local Database (Application-Specific)**
- Each application (scraping, analytics, workflows) maintains its own database in its directory
- Purpose:
  - Maintains data in its original format
  - Allows direct application-specific operations
  - Preserves raw data integrity
- Example structure:
```python
# apps/scraping/models.py
class RawScrapedData(models.Model):
    source = models.CharField(max_length=100)  # e.g., "facebook", "twitter"
    raw_content = models.JSONField()  # Keeps original format
    scraped_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField()  # Source-specific metadata
```

2. **Global Database (ML & Analytics)**
- Centralized data storage in `data/` directory
- Purpose:
  - ML model training
  - Cross-project analytics
  - System-wide data access
- Example structure:
```python
# apps/analytics/models.py
class GlobalMLData(models.Model):
    source_app = models.CharField(max_length=100)  # Origin application
    data_type = models.CharField(max_length=50)    # "text", "market", etc.
    processed_content = models.JSONField()         # Standardized format
    created_at = models.DateTimeField(auto_now_add=True)
    features = models.JSONField()                  # ML-ready features
```

*** Data Flow ***
```python
# services/data_service.py
class DataService:
    async def process_raw_data(self, data: Dict, source_app: str) -> Dict:
        """Handle dual storage of data"""
        try:
            # 1. Store in local app database
            local_data = RawScrapedData.objects.create(
                source=source_app,
                raw_content=data,
                metadata=self._extract_metadata(data)
            )
            
            # 2. Process and store in global ML database
            processed_data = self._standardize_format(data)
            global_data = GlobalMLData.objects.create(
                source_app=source_app,
                data_type=self._determine_data_type(data),
                processed_content=processed_data,
                features=self._extract_ml_features(processed_data)
            )
            
            return {
                'local_id': local_data.id,
                'global_id': global_data.id,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"Data processing error: {str(e)}")
            raise
```

4. **Benefits**:
- Applications maintain autonomy with their own data
- ML systems get standardized data for training
- No data loss from original sources
- Efficient querying for specific use cases
- Clear separation of concerns

5. **Example Usage**:
```python
# Local database query (application-specific)
facebook_posts = RawScrapedData.objects.filter(
    source='facebook',
    scraped_at__gte=yesterday
).values('raw_content')

# Global database query (ML training)
training_data = GlobalMLData.objects.filter(
    data_type='text',
    created_at__gte=last_month
).values('features')
```

This approach ensures that:
1. Applications can work with their native data structures
2. ML models get consistent, processed data
3. Original data is preserved
4. System can scale independently for different use cases



Data Workflow: Multi-Purpose Data Management
	1.	Raw Data Retention
Each project maintains its own local database within its respective directory under projects/applications/. This ensures that:
	•	Users can directly interact with the raw, unprocessed data specific to the application.
	•	Data is accessible in its native structure and format for the intended functionality of the project.

	2.	Global Data Consolidation
A copy of the data flows into the global data/ directory for ML training and cross-project analytics:
	•	Raw data: Stored under data/raw/ for system-wide ingestion.
	•	Processed data: Standardized and cleaned, ensuring consistency across projects.
	•	Validated data: Tagged for production use in ML pipelines.
This allows applications to contribute to a larger data ecosystem while maintaining their operational independence.
	
  3.	Bidirectional Data Sharing
	•	From Projects to ML: Data pipelines automatically push data from project-specific databases into the global data/ directory for aggregation and analysis.
	•	From ML to Projects: Insights or predictions generated by ML models are stored in project directories for user interaction.

User Interaction with Raw Data

For each application, raw data remains accessible for its core functionality. Examples include:
	•	Facebook Marketplace Monitor: Users can view live marketplace listings directly from the local database.
	•	News Summarizer: Users can access detailed summaries or filter content interactively based on the raw news feeds collected.
	•	Options Trading Bot: Real-time options data and risk insights are served from the project database, ensuring accuracy and immediacy.


## Data Processing Pipeline

### 1. Data Collection
- Applications collect raw data through various scrapers and APIs
- Each application maintains its own collection logic while adhering to global standards

### 2. Data Consolidation
All data flows through a standardized directory structure:
```
data/
├── raw/        # Initial unprocessed data from all sources
├── processed/  # Cleaned and normalized datasets
└── validated/  # Production-ready data for ML models
```

### 3. Machine Learning Workflow
The `ml/` directory manages the complete ML lifecycle:
- Model training using validated datasets
- Evaluation metrics and performance tracking
- Model versioning and deployment
- Continuous training pipelines

### 4. Monitoring and Feedback
Integrated monitoring system tracks:
- Data quality metrics
- Processing pipeline performance
- Model accuracy and drift
- System resource utilization
- User feedback and corrections

### 5. Deployment
The `deployment/` directory contains:
- Docker configurations for containerization
- Kubernetes manifests for orchestration
- Cloud infrastructure templates (AWS CDK)
- CI/CD pipeline configurations
- Environment-specific settings






Integrating MongoDB and SQL in your Data Science Framework can leverage the strengths of both database systems for different parts of the project. Here’s how they could interact and complement each other across the framework:

1. Data Collection & Processing

MongoDB:
	•	Raw Data Storage:
	•	MongoDB excels at handling diverse, unstructured data formats such as JSON-like data collected from APIs or web scraping. For example:
	•	Storing scraped Facebook Marketplace listings where each entry might have varying fields.
	•	Handling news articles with flexible structures and metadata.
	•	Real-time Data Streaming:
	•	MongoDB’s high write throughput is ideal for ingesting real-time data streams, such as financial API updates or live social media data.

SQL:
	•	Validation and Cleaning:
	•	After raw data is processed, cleaned, and standardized, SQL databases can store structured, relational data for further analysis.
	•	Example: Storing cleaned and validated financial data with fixed schemas like stock_id, price, and timestamp.
	•	Schema Enforcement:
	•	SQL databases ensure consistency when data relationships (e.g., foreign keys) are essential, such as linking user feedback to specific scraped articles.

2. Machine Learning & Analysis

MongoDB:
	•	NLP Content Analysis:
	•	MongoDB is ideal for storing and querying large volumes of text data for NLP tasks like sentiment and bias analysis.
	•	Example: Storing summarized news content with NLP analysis outputs.
	•	Training Data Aggregation:
	•	MongoDB can consolidate unstructured training datasets (e.g., raw text, images, logs) across multiple sources for machine learning pipelines.

SQL:
	•	Processed and Validated Data:
	•	SQL is better suited for storing processed and validated datasets used in machine learning models.
	•	Example: Storing normalized data for market prediction models in relational tables.
	•	Performance Tracking:
	•	SQL databases can store model evaluation metrics and performance logs for structured querying and reporting.

3. Deployment & Monitoring

MongoDB:
	•	Log Aggregation:
	•	MongoDB is ideal for storing unstructured logs and monitoring data like system health metrics and error logs.
	•	Example: Tracking pipeline performance and resource utilization.
	•	User Interaction:
	•	MongoDB can provide a backend for real-time applications, such as serving raw Facebook Marketplace data directly to users.

SQL:
	•	Audit Trails:
	•	SQL can store structured audit logs for sensitive operations, ensuring traceability.
	•	Example: Logging changes to validated datasets or tracking user feedback.
	•	Relational Data for Deployment:
	•	SQL databases can manage environment configurations and deployment settings in a structured way.

4. Workflow Integration

Bidirectional Data Sharing:
	•	From MongoDB to SQL:
	•	After raw data is collected and stored in MongoDB, it can be processed and moved to SQL for validation and analytics.
	•	Example: Scraped real estate data stored in MongoDB is cleaned and normalized, then transferred to SQL for investment scenario modeling.
	•	From SQL to MongoDB:
	•	Predictions or insights generated by ML models stored in SQL can be pushed back into MongoDB for use in real-time user-facing applications.
	•	Example: Storing trading recommendations in MongoDB to be served to a web app.

5. Examples of Specific Applications

News Summarizer:
	•	MongoDB:
	•	Storing raw articles and their metadata.
	•	Saving flexible NLP outputs like topic modeling and bias analysis.
	•	SQL:
	•	Storing structured summaries for query-based analysis or reporting.

Facebook Marketplace Monitor:
	•	MongoDB:
	•	Storing real-time listings with varying fields.
	•	SQL:
	•	Storing validated and structured insights, such as aggregated statistics on listing categories.

Options Trading Bot:
	•	MongoDB:
	•	Storing real-time market data and logs from APIs.
	•	SQL:
	•	Storing historical performance metrics and validated trading decisions.

Why Use Both Together?

Using MongoDB and SQL in tandem allows your framework to:
	1.	Handle unstructured data (MongoDB) while enforcing relational integrity for structured data (SQL).
	2.	Scale horizontally for high-throughput tasks (MongoDB) while supporting advanced querying and analytics (SQL).
	3.	Enable real-time interactivity (MongoDB) while ensuring data consistency and traceability (SQL).

By strategically assigning tasks to each database type, your framework can maximize efficiency, scalability, and maintainability.

## Prerequisites

### System Requirements
- Python 3.9+
- Node.js 16+
- Docker
- Kubernetes (optional)
- AWS Account (for cloud deployment)

### API Keys Required
- OpenAI API (GPT-4/Claude)
- TD Ameritrade API
- Facebook API (optional)
- News API services

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/data-framework.git
cd data-framework
```

2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
npm install  # For frontend components
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys and configurations
```

5. Initialize the database:
```bash
python manage.py migrate
```

## Development

### Running Locally
```bash
# Backend
python manage.py runserver

# Frontend
npm start

# Docker
docker-compose up
```

### Testing
```bash
# Backend tests
pytest

# Frontend tests
npm test

# Integration tests
pytest tests/integration
```

## Deployment

### Docker Deployment
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes Deployment
```bash
kubectl apply -f deployment/kubernetes/
```

### AWS Deployment
```bash
cd infrastructure
cdk deploy
```

## Documentation

Each application includes detailed documentation:
- [News Summarizer Documentation](projects/applications/news-summary/README.md)
- [Facebook Marketplace Documentation](projects/applications/facebook-market/README.md)
- [Property Analysis Documentation](projects/applications/property-analysis/README.md)
- [Options Trading Documentation](projects/applications/options-trader/README.md)
- [Text Analysis Documentation](projects/applications/text-analysis/README.md)
- [Listing Bot Documentation](projects/applications/listing-bot/README.md)
