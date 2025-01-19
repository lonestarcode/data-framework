Core machine learning infrastructure managing model lifecycle, training pipelines, and analytics workflows. Integrates with Spring Boot backend for orchestration and dual database system for data management.

## Directory Structure

```
ml_analytics/
├── models/
│   ├── base/                  # Base interfaces and abstractions
│   ├── experimental/          # Research and testing
│   ├── production/           # Production models by domain
│   │   ├── market/          # Market analysis models
│   │   ├── nlp/             # Natural language models
│   │   └── vision/          # Computer vision models
│   └── trained/             # Trained model artifacts by stage
├── pipelines/
│   ├── training/            # Training workflows
│   ├── evaluation/          # Testing and validation
│   └── deployment/          # Production deployment
├── shared/                  # Shared resources
│   ├── artifacts/          # Model artifacts
│   ├── configs/            # Configuration files
│   ├── experiments/        # Experiment tracking
│   ├── governance/         # Model governance
│   └── lineage/           # Model lineage tracking
└── registry/              # Model registry
```

## Framework Integration

### Data Flow
1. **Input**: Receives processed data from global data directory
```typescript:data/README.md
startLine: 6
endLine: 18
```

2. **Processing**: Integrates with core analytics pipelines
```typescript:applications/core_analytics/README.md
startLine: 118
endLine: 131
```

3. **Output**: Deploys models via Spring Boot orchestration
```typescript:backend/README.md
startLine: 81
endLine: 110
```

## Core Components

### 1. Model Registry
- Version control for ML models
- Model lineage tracking
- Metadata management
- Deployment status tracking

### 2. Training Pipelines
- Continuous training workflows
- Fine-tuning capabilities
- Adaptive learning through metadata
- Validation gates and quality checks

### 3. Evaluation System
- Performance metrics tracking
- Model drift detection
- A/B testing framework
- Resource utilization monitoring

## Database Integration

### MongoDB
- Training data storage
- Unstructured analytics
- Model predictions
- Real-time features

### SQL
- Validated metrics
- Performance tracking
- Model metadata
- Audit trails

## Usage

### Model Training
```python
from ml_analytics.pipelines import ModelTrainer
from ml_analytics.models.base import BaseModel

class MarketModel(BaseModel):
    def train(self, data):
        # Implementation
        pass

trainer = ModelTrainer()
trainer.train_and_evaluate(MarketModel(), data)
```

### Model Registry
```python
from ml_analytics.registry import ModelRegistry

registry = ModelRegistry()
registry.register_model('market_predictor', model, version='1.0')
```

## Prerequisites
- Python 3.9+
- Spring Boot backend service
- MongoDB & PostgreSQL
- Required Python packages in requirements.txt

## Getting Started
1. Install dependencies
2. Configure database connections
3. Set up Spring Boot integration
4. Initialize model registry

