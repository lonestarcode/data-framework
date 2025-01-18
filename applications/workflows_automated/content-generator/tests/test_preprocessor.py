import pytest
from datetime import datetime
from src.pipeline.preprocessor import ContentPreprocessor

class TestContentPreprocessor:
    @pytest.fixture
    def preprocessor(self):
        return ContentPreprocessor()

    @pytest.fixture
    def valid_summary(self):
        return {
            'summary_text': 'Test summary content.',
            'source': 'TestSource',
            'url': 'https://test.com/article',
            'timestamp': datetime.now().isoformat(),
            'sentiment_analysis': {'positive': 0.7, 'negative': 0.3},
            'bias_analysis': {'political': 0.2},
            'keywords': ['test', 'summary']
        }

    def test_preprocess_valid_summary(self, preprocessor, valid_summary):
        result = preprocessor.preprocess_summaries([valid_summary])
        
        assert len(result) == 1
        processed = result[0]
        
        assert 'processed_text' in processed
        assert 'source_metadata' in processed
        assert 'analysis_data' in processed
        assert processed['source_metadata']['url'] == valid_summary['url']
        assert processed['source_metadata']['source'] == valid_summary['source']
        assert len(processed['analysis_data']['keywords']) == 2

    def test_preprocess_missing_required_fields(self, preprocessor):
        invalid_summary = {
            'summary_text': 'Test content',
            # Missing 'source' and 'url'
        }
        
        result = preprocessor.preprocess_summaries([invalid_summary])
        assert len(result) == 0

    def test_clean_text(self, preprocessor):
        dirty_text = "This   is  a    messy... text   with   spaces..."
        cleaned = preprocessor._clean_text(dirty_text)
        assert cleaned == "This is a messy. text with spaces."
        assert "  " not in cleaned
        assert "..." not in cleaned

    def test_validate_summary(self, preprocessor, valid_summary):
        assert preprocessor._validate_summary(valid_summary) == True
        
        invalid_summary = valid_summary.copy()
        del invalid_summary['url']
        assert preprocessor._validate_summary(invalid_summary) == False

    def test_preprocess_empty_summaries(self, preprocessor):
        with pytest.raises(ValueError) as exc_info:
            preprocessor.preprocess_summaries([])
        assert "No valid summaries to process" in str(exc_info.value)

    def test_preprocess_multiple_summaries(self, preprocessor, valid_summary):
        summaries = [
            valid_summary,
            {**valid_summary, 'url': 'https://test.com/article2'},
            {'summary_text': 'Invalid summary'}  # Should be filtered out
        ]
        
        result = preprocessor.preprocess_summaries(summaries)
        assert len(result) == 2  # Only valid summaries should be processed
        assert result[0]['source_metadata']['url'] != result[1]['source_metadata']['url']

    @pytest.mark.parametrize("text,expected", [
        ("Normal text.", "Normal text."),
        ("Text   with   spaces", "Text with spaces"),
        ("Text... with... dots...", "Text. with. dots."),
        ("", ""),
        ("   Padded   text   ", "Padded text")
    ])
    def test_clean_text_variations(self, preprocessor, text, expected):
        assert preprocessor._clean_text(text) == expected