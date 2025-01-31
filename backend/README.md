
# Backend Service

A Spring Boot-based orchestration layer that coordinates data flow, analytics processing, and automated workflows across the entire data science framework.

## Overview
This backend service manages and orchestrates Python-based applications for:
- Data scraping and collection
- Analytics and ML processing
- Automated workflow execution
- System monitoring and logging

## Structure
- `src/main/java/com/dataframework/`
  - `config/`: Spring configurations for databases, Python integration
  - `controller/`: REST API endpoints
  - `service/`: Business logic and service coordination
  - `model/`: Data models and entities
  - `repository/`: Data access interfaces
  - `orchestration/`: Python service coordination

## Features
- Python service orchestration
- Dual database management (MongoDB & SQL)
- Centralized API gateway
- ML model deployment coordination
- Task scheduling and monitoring
- Cross-application data flow
- Performance tracking
- Error handling and recovery

## Data Management
- MongoDB: Unstructured data, real-time operations
- PostgreSQL: Structured data, analytics results
- Python script execution management
- Cache coordination
- Database migrations

## Prerequisites
- Java 17+
- Python 3.9+
- MongoDB
- PostgreSQL
- Maven

## Configuration
- Database connections
- Python environment settings
- API configurations
- Monitoring parameters
- Logging preferences

## Integration Points
- Python scraping applications
- Analytics processing pipelines
- ML model training and deployment
- Automated workflow execution
- System monitoring and metrics

## Development
1. Build the project:
```bash
mvn clean install
```

2. Run the application:
```bash
mvn spring-boot:run
```

3. Access the API:
```
http://localhost:8080/api/v1/
```




2. **Key Components to Create**:

a. **Python Service Interface** (Java):
```java
@Service
public class PythonServiceOrchestrator {
    private final ProcessBuilder processBuilder;
    
    public CompletableFuture<ProcessResult> executePythonScript(String scriptPath, Map<String, String> params) {
        // Execute Python scripts asynchronously
        // Monitor execution
        // Handle results
    }
}
```

b. **Workflow Orchestration** (Java):
```java
@Service
public class WorkflowOrchestrator {
    private final PythonServiceOrchestrator pythonService;
    private final MongoTemplate mongoTemplate;
    private final JdbcTemplate jdbcTemplate;

    public void orchestrateDataFlow(String dataType, Map<String, Object> data) {
        // 1. Trigger Python scraping
        // 2. Coordinate analysis
        // 3. Manage ML training
        // 4. Handle automated workflows
    }
}
```

3. **Database Integration**:
References the dual database approach from:

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
```


4. **Python Script Management**:
Keep Python scripts for:
- Scraping (reference from):

```7:10:applications/advanced_scraping/facebook-scrape/README.md
- **Multi-Strategy Scraping**:
  - Dynamic scraping for JavaScript-rendered pages (Selenium/Playwright).
  - API integration using Facebook GraphQL (if accessible).
  - Static scraping for basic HTTP-based pages.
```


- Analytics (reference from):

```43:49:applications/core_scraping/text-scrape/README.md
### Content Filtering
- **Advisory Filters**
  - Reliability assessment
  - Sentiment analysis
- **Prohibitive Filters**
  - Content validation
  - Quality checks
```


- ML Training (reference from):

```167:173:README.md
### 3. Machine Learning Workflow
The `ml/` directory manages the complete ML lifecycle:
- Model training using validated datasets
- Evaluation metrics and performance tracking
- Model versioning and deployment
- Continuous training pipelines

```


5. **Required Changes**:

a. Update all Python scripts to accept CLI arguments and return standardized JSON outputs

b. Create Spring Boot configurations for:
- Python environment management
- Script execution
- Result parsing
- Error handling

c. Move orchestration logic from:

```18:26:applications/workflows_automated/README.md
## Features
- Automated task scheduling
- Multi-platform integration
- Content generation and posting
- Error handling and recovery
- Performance monitoring
- Result tracking
- Configuration management

```

to Spring Boot services

6. **Dependencies** (pom.xml):
```xml
<dependencies>
    <!-- Spring Boot -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    
    <!-- Database -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-mongodb</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    
    <!-- Python Integration -->
    <dependency>
        <groupId>org.python</groupId>
        <artifactId>jython-standalone</artifactId>
        <version>2.7.3</version>
    </dependency>
</dependencies>
```

