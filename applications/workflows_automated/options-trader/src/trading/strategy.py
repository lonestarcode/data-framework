from typing import Dict, List, Optional
from datetime import datetime, time
import logging
from .position import Position
from .risk import RiskManager

class OptionsStrategy:
    def __init__(self, config: Dict):
        self.config = config
        self.risk_manager = RiskManager(config)
        self.open_positions: List[Position] = []
        self.logger = logging.getLogger(__name__)
        
    def generate_trade_signals(self, analysis: Dict, market_data: Dict) -> List[Dict]:
        """Generate trading signals based on GPT analysis and market data"""
        try:
            if not self._is_trading_time():
                return []
                
            if not self._can_open_new_positions():
                return []
                
            signals = []
            
            # Check if analysis confidence meets minimum threshold
            if analysis['confidence'] < self.config.get('min_confidence', 0.7):
                self.logger.info(f"Analysis confidence too low: {analysis['confidence']}")
                return signals
                
            # Generate potential trades based on analysis
            potential_trade = self._evaluate_trading_opportunity(analysis, market_data)
            if potential_trade:
                # Validate trade against risk parameters
                if self.risk_manager.validate_trade(potential_trade, self.open_positions):
                    signals.append(potential_trade)
                    self.logger.info(f"Generated trade signal: {potential_trade}")
                
            return signals
            
    def _evaluate_trading_opportunity(self, analysis: Dict, market_data: Dict) -> Optional[Dict]:
        """Evaluate and create specific option trade based on analysis"""
        try:
            # Extract key metrics from analysis
            sentiment = analysis.get('sentiment', 'neutral')
            volatility_outlook = analysis.get('volatility_outlook', 'neutral')
            time_horizon = analysis.get('time_horizon', 'medium')
            
            # Determine strategy type based on analysis
            strategy_type = self._select_strategy_type(sentiment, volatility_outlook, time_horizon)
            
            if not strategy_type:
                return None
                
            # Build trade parameters
            trade = {
                'strategy_type': strategy_type,
                'direction': 'long' if sentiment == 'bullish' else 'short',
                'symbol': market_data['symbol'],
                'position_size': self._calculate_position_size(market_data),
                'entry_price': market_data['price'],
                'stop_loss': self._calculate_stop_loss(market_data),
                'take_profit': self._calculate_take_profit(market_data),
                'expiration': self._select_expiration(time_horizon),
                'strike_selection': self._select_strikes(strategy_type, market_data),
                'timestamp': datetime.now().isoformat()
            }
            
            return trade
            
        except Exception as e:
            self.logger.error(f"Error evaluating trading opportunity: {str(e)}")
            return None
            
    def _select_strategy_type(self, sentiment: str, volatility_outlook: str, time_horizon: str) -> Optional[str]:
        """Select appropriate options strategy based on market analysis"""
        if sentiment == 'bullish':
            if volatility_outlook == 'high':
                return 'credit_put_spread'
            elif volatility_outlook == 'low':
                return 'long_call'
        elif sentiment == 'bearish':
            if volatility_outlook == 'high':
                return 'credit_call_spread'
            elif volatility_outlook == 'low':
                return 'long_put'
        
        return None
        
    def _calculate_position_size(self, market_data: Dict) -> float:
        """Calculate appropriate position size based on risk parameters"""
        account_size = self.config.get('account_size', 100000)
        risk_per_trade = self.config.get('risk_per_trade', 0.01)
        max_position_size = self.config.get('max_position_size', 5000)
        
        position_size = account_size * risk_per_trade
        return min(position_size, max_position_size)
        
    def _calculate_stop_loss(self, market_data: Dict) -> float:
        """Calculate stop loss price based on market conditions"""
        stop_loss_percent = self.config.get('stop_loss_percent', 0.01)
        if market_data.get('direction') == 'long':
            return market_data['price'] * (1 - stop_loss_percent)
        return market_data['price'] * (1 + stop_loss_percent)
        
    def _calculate_take_profit(self, market_data: Dict) -> float:
        """Calculate take profit price based on risk/reward ratio"""
        take_profit_percent = self.config.get('take_profit_percent', 0.02)
        if market_data.get('direction') == 'long':
            return market_data['price'] * (1 + take_profit_percent)
        return market_data['price'] * (1 - take_profit_percent)
        
    def _select_expiration(self, time_horizon: str) -> int:
        """Select appropriate option expiration based on time horizon"""
        horizon_mapping = {
            'short': 30,    # 30 days
            'medium': 60,   # 60 days
            'long': 90      # 90 days
        }
        return horizon_mapping.get(time_horizon, 45)
        
    def _select_strikes(self, strategy_type: str, market_data: Dict) -> Dict:
        """Select appropriate strike prices based on strategy"""
        current_price = market_data['price']
        
        if strategy_type == 'long_call':
            return {'strike': current_price * 1.01}  # Slightly OTM
        elif strategy_type == 'long_put':
            return {'strike': current_price * 0.99}  # Slightly OTM
        elif strategy_type == 'credit_put_spread':
            return {
                'short_strike': current_price * 0.95,
                'long_strike': current_price * 0.93
            }
        elif strategy_type == 'credit_call_spread':
            return {
                'short_strike': current_price * 1.05,
                'long_strike': current_price * 1.07
            }
            
    def _is_trading_time(self) -> bool:
        """Check if current time is within trading hours"""
        now = datetime.now().time()
        market_open = time(9, 30)  # 9:30 AM
        market_close = time(16, 0)  # 4:00 PM
        return market_open <= now <= market_close
        
    def _can_open_new_positions(self) -> bool:
        """Check if we can open new positions based on current risk limits"""
        max_positions = self.config.get('max_positions', 3)
        return len(self.open_positions) < max_positions