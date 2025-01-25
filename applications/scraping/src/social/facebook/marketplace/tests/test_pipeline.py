import pytest
from src.pipeline.data_pipeline import MarketplacePipeline

def test_pipeline_initialization():
    pipeline = MarketplacePipeline()
    assert pipeline is not None
