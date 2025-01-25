# Text Analytics

Advanced text analysis module with configurable models, processing pipelines, and comprehensive evaluation tools.

## 🏗 Directory Structure

```
text-analytics/
├── api/                      # API endpoints
│   └── endpoints/
│       ├── analysis.py      # Analysis endpoints
│       ├── models.py        # Model management
│       └── pipelines.py     # Pipeline control
├── config/                   # Configuration files
│   ├── models/              # Model settings
│   │   ├── entity.yaml      # Entity recognition config
│   │   ├── pattern.yaml     # Pattern detection config
│   │   └── semantic.yaml    # Semantic analysis config
│   ├── pipelines/           # Pipeline settings
│   └── monitoring/          # Metrics configuration
├── data/                     # Data storage
│   ├── processed/           # Analysis results
│   ├── training/            # Training datasets
│   └── evaluation/          # Evaluation results
└── src/                      # Source code
    ├── analyzers/           # Analysis components
    │   ├── base_text_analyzer.py
    │   ├── sentiment_analyzer.py
    │   └── topic_analyzer.py
    ├── models/              # Model implementations
    │   ├── entity/          # Entity analysis
    │   ├── pattern/         # Pattern detection
    │   └── semantic/        # Semantic analysis
    ├── pipelines/           # Processing pipelines
    ├── processors/          # Data processors
    ├── enrichment/          # Data enrichment
    ├── visualization/       # Result visualization
    └── evaluation/          # Performance metrics
```

## 🚀 Features

### Analysis Capabilities
- **Sentiment Analysis**
  - Text sentiment scoring
  - Emotion detection
  - Opinion mining

- **Topic Analysis**
  - Topic extraction
  - Theme clustering
  - Keyword identification

- **Entity Recognition**
  - Named entity detection
  - Relationship mapping
  - Entity linking

- **Pattern Detection**
  - Trend analysis
  - Anomaly detection
  - Correlation finding

- **Semantic Analysis**
  - Context understanding
  - Theme extraction
  - Relationship detection

### Processing Pipeline
- Configurable processing steps
- Batch and stream processing
- Data enrichment
- Result validation

## 🛠 Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure models:
```bash
# Update model configurations
vi config/models/entity.yaml
vi config/models/pattern.yaml
vi config/models/semantic.yaml
```

3. Configure pipeline:
```bash
# Set pipeline parameters
vi config/pipelines/pipeline_config.yaml
```

## 🔄 Usage

### Basic Analysis
```python
from src.analyzers import SentimentAnalyzer, TopicAnalyzer

# Sentiment Analysis
async with SentimentAnalyzer() as analyzer:
    sentiment = await analyzer.analyze(text)

# Topic Analysis
async with TopicAnalyzer() as analyzer:
    topics = await analyzer.analyze(documents)
```

### Pipeline Processing
```python
from src.pipelines import TextPipeline
from src.processors import TextProcessor

# Configure pipeline
pipeline = TextPipeline([
    TextProcessor(),
    SentimentAnalyzer(),
    TopicAnalyzer()
])

# Process batch
results = await pipeline.process_batch(texts)
```

### Visualization
```python
from src.visualization import PlotGenerator

# Generate visualizations
plotter = PlotGenerator()
plotter.plot_sentiment_distribution(results)
plotter.plot_topic_clusters(topics)
```

## 📊 Data Flow

1. **Input Processing**
   - Text cleaning
   - Feature extraction
   - Data validation

2. **Analysis**
   - Model application
   - Pattern detection
   - Result generation

3. **Post-Processing**
   - Result validation
   - Data enrichment
   - Visualization

## ⚙️ Configuration Examples

### Entity Model Config
```yaml
model:
  name: "entity-recognizer"
  type: "transformer"
  parameters:
    batch_size: 32
    max_length: 512
```

### Pipeline Config
```yaml
pipeline:
  steps:
    - name: "text_processor"
      config:
        clean_text: true
        extract_features: true
    - name: "sentiment_analyzer"
      config:
        threshold: 0.5
    - name: "topic_analyzer"
      config:
        num_topics: 10
```

## 📈 Evaluation

### Performance Metrics
- Accuracy
- Precision
- Recall
- F1 Score
- Processing Time

### Quality Assessment
- Result validation
- Confidence scoring
- Error analysis
- Performance tracking

## 🔍 Monitoring

- Real-time metrics
- Error tracking
- Resource usage
- Quality control

## 🧪 Testing

Run tests:
```bash
pytest tests/
```

## 📚 Documentation

Detailed documentation available for:
- API Reference
- Model Documentation
- Pipeline Configuration
- Evaluation Metrics