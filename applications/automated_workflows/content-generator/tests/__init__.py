import pytest
import sys
from pathlib import Path

# Add src directory to Python path for tests
src_path = Path(__file__).parent.parent / 'src'
sys.path.append(str(src_path))

# Test fixtures and utilities can be defined here
@pytest.fixture
def test_config():
    return {
        'llm': {
            'api_key': 'test-key',
            'model': 'test-model'
        },
        'style_guide': {
            'tone': 'professional',
            'max_paragraphs': 5
        }
    }
