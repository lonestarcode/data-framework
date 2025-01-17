import openai
from typing import Dict
import logging

class GPTAnalyzer:
    def __init__(self, config: Dict):
        self.config = config
        openai.api_key = config['api_key']
        self.logger = logging.getLogger(__name__)
        
    async def analyze_market_conditions(self, market_data: Dict) -> Dict:
        try:
            prompt = self._build_analysis_prompt(market_data)
            
            response = await openai.chat.completions.create(
                model=self.config['model'],
                messages=[
                    {
                        "role": "system",
                        "content": "You are an options trading analyst. Analyze the given market data and provide trading signals."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.config['temperature'],
                max_tokens=self.config['max_tokens']
            )
            
            return self._parse_gpt_response(response.choices[0].message.content)
            
        except Exception as e:
            self.logger.error(f"GPT analysis error: {str(e)}")
            raise
            
    def _build_analysis_prompt(self, market_data: Dict) -> str:
        return f"""
        Analyze the following market data for options trading opportunities:
        
        Stock Price: ${market_data['price']}
        IV Percentile: {market_data['iv_percentile']}%
        RSI: {market_data['rsi']}
        MACD: {market_data['macd']}
        Volume: {market_data['volume']}
        
        Consider:
        1. Current market conditions
        2. Technical indicators
        3. Implied volatility levels
        4. Risk/reward ratio
        
        Provide specific options trading recommendations.
        """