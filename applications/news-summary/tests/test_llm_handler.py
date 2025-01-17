import pytest
from src.pipeline.llm_handler import GPT4Handler, ClaudeHandler
import openai
from anthropic import Anthropic

class TestGPT4Handler:
    @pytest.fixture
    def handler(self):
        return GPT4Handler("test-key")

    def test_generate_summary(self, handler, monkeypatch):
        mock_response = type('obj', (object,), {
            'choices': [type('obj', (object,), {
                'message': type('obj', (object,), {
                    'content': 'Test summary'
                })
            })]
        })
        
        monkeypatch.setattr(openai.chat.completions, "create", lambda **kwargs: mock_response)
        
        result = handler.generate_summary("Test text")
        assert result["summary"] == "Test summary"
        assert result["model"] == "gpt-4"

class TestClaudeHandler:
    @pytest.fixture
    def handler(self):
        return ClaudeHandler("test-key")

    def test_generate_summary(self, handler, monkeypatch):
        mock_response = type('obj', (object,), {
            'content': [type('obj', (object,), {'text': 'Test summary'})]
        })
        
        monkeypatch.setattr(Anthropic, "messages", type('obj', (object,), {
            'create': lambda **kwargs: mock_response
        }))
        
        result = handler.generate_summary("Test text")
        assert result["summary"] == "Test summary"
        assert result["model"] == "claude-3" 