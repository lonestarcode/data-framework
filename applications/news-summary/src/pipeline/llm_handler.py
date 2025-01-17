from typing import Dict, List
import openai
from anthropic import Anthropic
from abc import ABC, abstractmethod

class LLMHandler(ABC):
    @abstractmethod
    def generate_summary(self, text: str, source: str) -> Dict[str, str]:
        pass

class GPT4Handler(LLMHandler):
    def __init__(self, api_key: str):
        openai.api_key = api_key
        
    def generate_summary(self, text: str, source: str) -> Dict[str, str]:
        prompt = f"""
        Generate a concise summary of the following article from {source}.
        Include source attribution and extract 3-5 relevant keyword tags.
        
        Article: {text}
        """
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Generate a concise summary with source attribution."},
                {"role": "user", "content": prompt}
            ]
        )
        return {
            "summary": response.choices[0].message.content,
            "model": "gpt-4"
        }

class ClaudeHandler(LLMHandler):
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        
    def generate_summary(self, text: str, source: str) -> Dict[str, str]:
        prompt = f"""
        Generate a concise summary of the following article from {source}.
        Include source attribution and extract 3-5 relevant keyword tags.
        
        Article: {text}
        """
        response = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        return {
            "summary": response.content[0].text,
            "model": "claude-3"
        } 