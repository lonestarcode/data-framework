from typing import Dict, List, Optional
from datetime import datetime
import logging
import numpy as np

class RiskManager:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize risk limits
        self.max_position_size = config.get('max_position_size', 5000)
        self.max_portfolio_risk = config.get('max_portfolio_risk', 0.02)  # 2% max portfolio risk
        self.max_correlation = config.get('max_correlation', 0.7)
        self.max_positions = config.get('max_positions', 3)
        self.max_sector_exposure = config.get('max_sector_exposure', 0.30)  # 30% max sector exposure
        
        # Daily tracking
        self.daily_loss = 0
        self.daily_trades = 0
        self.last_reset = datetime.now().date()
        
    def validate_trade(self, trade: Dict, current_positions: List[Dict]) -> bool:
        """Validate if a trade meets all risk management criteria"""
        try:
            # Reset daily tracking if needed
            self._reset_daily_tracking()
            
            # Run all risk checks
            checks = [
                self._check_position_size(trade),
                self._check_portfolio_risk(trade, current_positions),
                self._check_correlation_risk(trade, current_positions),
                self._check_sector_exposure(trade, current_positions),
                self._check_daily_limits(trade)
            ]
            
            # Trade is valid only if all checks pass
            is_valid = all(checks)
            
            if not is_valid:
                self.logger.warning(f"Trade validation failed for {trade['symbol']}")
            
            return is_valid
            
        except Exception as e:
            self.logger.error(f"Error in trade validation: {str(e)}")
            return False
            
    def update_daily_metrics(self, pnl: float):
        """Update daily profit/loss tracking"""
        self.daily_loss = min(0, self.daily_loss + pnl)
        self.daily_trades += 1
        
    def _reset_daily_tracking(self):
        """Reset daily tracking if it's a new day"""
        current_date = datetime.now().date()
        if current_date > self.last_reset:
            self.daily_loss = 0
            self.daily_trades = 0
            self.last_reset = current_date
            
    def _check_position_size(self, trade: Dict) -> bool:
        """Verify trade size is within limits"""
        if trade['position_size'] > self.max_position_size:
            self.logger.warning(f"Position size {trade['position_size']} exceeds maximum {self.max_position_size}")
            return False
        return True
        
    def _check_portfolio_risk(self, trade: Dict, current_positions: List[Dict]) -> bool:
        """Check if trade would exceed portfolio risk limits"""
        try:
            # Calculate current portfolio risk
            current_risk = sum(pos['risk_amount'] for pos in current_positions)
            
            # Calculate new trade risk
            new_trade_risk = self._calculate_trade_risk(trade)
            
            # Calculate total portfolio value (should be provided by broker in real implementation)
            portfolio_value = self.config.get('portfolio_value', 100000)
            
            # Calculate total risk percentage
            total_risk_pct = (current_risk + new_trade_risk) / portfolio_value
            
            if total_risk_pct > self.max_portfolio_risk:
                self.logger.warning(f"Portfolio risk {total_risk_pct:.2%} would exceed maximum {self.max_portfolio_risk:.2%}")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking portfolio risk: {str(e)}")
            return False
            
    def _check_correlation_risk(self, trade: Dict, current_positions: List[Dict]) -> bool:
        """Check correlation with existing positions"""
        try:
            if not current_positions:
                return True
                
            # This would typically use real correlation data from a market data provider
            for position in current_positions:
                if self._calculate_correlation(trade['symbol'], position['symbol']) > self.max_correlation:
                    self.logger.warning(f"High correlation detected between {trade['symbol']} and {position['symbol']}")
                    return False
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking correlation risk: {str(e)}")
            return False
            
    def _check_sector_exposure(self, trade: Dict, current_positions: List[Dict]) -> bool:
        """Check sector exposure limits"""
        try:
            # Get sector for new trade (would come from market data provider)
            sector = self._get_sector(trade['symbol'])
            
            # Calculate current sector exposure
            sector_positions = [p for p in current_positions if self._get_sector(p['symbol']) == sector]
            sector_exposure = sum(p['position_size'] for p in sector_positions)
            
            # Calculate total portfolio value
            portfolio_value = self.config.get('portfolio_value', 100000)
            
            # Check if new trade would exceed sector limits
            new_exposure = (sector_exposure + trade['position_size']) / portfolio_value
            
            if new_exposure > self.max_sector_exposure:
                self.logger.warning(f"Sector exposure {new_exposure:.2%} would exceed maximum {self.max_sector_exposure:.2%}")
                return False
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking sector exposure: {str(e)}")
            return False
            
    def _check_daily_limits(self, trade: Dict) -> bool:
        """Check if daily loss or trade limits would be exceeded"""
        max_daily_loss = self.config.get('max_daily_loss', 1000)
        max_daily_trades = self.config.get('max_daily_trades', 10)
        
        if abs(self.daily_loss) >= max_daily_loss:
            self.logger.warning(f"Daily loss limit {max_daily_loss} reached")
            return False
            
        if self.daily_trades >= max_daily_trades:
            self.logger.warning(f"Daily trade limit {max_daily_trades} reached")
            return False
            
        return True
        
    def _calculate_trade_risk(self, trade: Dict) -> float:
        """Calculate risk amount for a trade"""
        entry = trade['entry_price']
        stop_loss = trade['stop_loss']
        position_size = trade['position_size']
        
        return abs(entry - stop_loss) * position_size
        
    def _calculate_correlation(self, symbol1: str, symbol2: str) -> float:
        """Calculate correlation between two symbols"""
        # This would typically use real market data
        # Placeholder implementation
        return 0.5
        
    def _get_sector(self, symbol: str) -> str:
        """Get sector for a symbol"""
        # This would typically use market data provider
        # Placeholder implementation
        return "Technology"