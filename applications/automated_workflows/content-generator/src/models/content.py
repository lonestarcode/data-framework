from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Article:
    topic: str
    content: str
    sources: List[str]
    generated_at: datetime
    sentiment_scores: Dict[str, float]
    keywords: List[str]
    bias_metrics: Dict[str, float]
    model_used: str
    status: str = "success"

@dataclass
class GenerationMetrics:
    coherence_score: float
    readability_score: float
    source_diversity: float
    topic_relevance: float