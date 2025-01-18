# Text Analysis Framework

Advanced Natural Language Processing (NLP) pipeline for processing and analyzing textual data. Integrates multiple analysis types including summarization, sentiment analysis, topic modeling, bias detection, and language identification.

## 🎯 Purpose

Text-Analysis serves as the central processing hub for all text data in the framework, providing:
- Text summarization using GPT models
- Sentiment analysis and emotional tone detection
- Topic modeling and theme clustering
- Bias detection and analysis
- Language identification and validation

## 🏗 Architecture

The project is organized into specialized modules:

```
analysis-text/
├── models/                    # Core analysis models
│   ├── summarization/        # Text summarization
│   ├── sentiment_analysis/   # Sentiment detection
│   ├── topic_modeling/       # Topic identification
│   ├── bias_analysis/       # Bias detection
│   └── language_detection/  # Language identification
├── data/                    # Data management
│   ├── raw/                # Input data
│   ├── processed/          # Cleaned data
│   └── analysis_logs/      # Analysis results
└── src/                    # Source code
    └── api/               # API endpoints
```

## 🚀 Features

### 1. Text Summarization
```python
response = requests.post('http://localhost:5000/summarize',
                        json={'text': 'Your long article text here'})
# Returns: {'summary': 'Concise summary of the article'}
```

### 2. Sentiment Analysis
```python
response = requests.post('http://localhost:5000/analyze_sentiment',
                        json={'text': 'I love this product!'})
# Returns: {'sentiment': 'positive', 'score': 0.89}
```

### 3. Topic Modeling
```python
response = requests.post('http://localhost:5000/analyze_topics',
                        json={'texts': ['AI article', 'Sports news']})
# Returns: {'topics': ['technology', 'sports']}
```

### 4. Bias Detection
```python
response = requests.post('http://localhost:5000/analyze_bias',
                        json={'text': 'Article content'})
# Returns: {'bias_score': 0.23, 'bias_type': 'minimal'}
```

### 5. Language Detection
```python
response = requests.post('http://localhost:5000/detect_language',
                        json={'text': 'Hello world'})
# Returns: {'language': 'en', 'confidence': 0.98}
```

## 📋 Requirements

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

Each analysis module has its own configuration in `models/[module]/config.py`:
- Summarization parameters
- Sentiment thresholds
- Topic modeling settings
- Bias detection rules
- Language detection configs

## 🏃‍♂️ Usage

### Running Analysis Pipelines
```bash
# Run specific analysis
./scripts/run_summarization.py
./scripts/run_sentiment_analysis.py
./scripts/run_topic_analysis.py
./scripts/run_bias_analysis.py
./scripts/run_lang_detection.py

# Run complete pipeline
./scripts/run_full_pipeline.sh
```

### Data Processing
```bash
# Preprocess data
python scripts/preprocess_data.py --module summarization
python scripts/preprocess_data.py --module sentiment
```

## 🔄 Integration Points

### Input
- Raw text from scrape-text
- Direct API submissions
- Batch file processing

### Output
- Processed results in data/[module]/analysis_logs/
- API endpoints for each analysis type
- Integration with content-generator

## 📊 Monitoring

Monitor analysis performance:
```bash
python scripts/check_performance.py --module summarization
python scripts/check_performance.py --module sentiment
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Test specific module
pytest tests/test_summarization.py
pytest tests/test_sentiment.py
```

## 🔒 Security

- API authentication required
- Rate limiting implemented
- Input validation
- Error handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.