from typing import Dict, Optional
from datetime import datetime
from enum import Enum
import logging

class PositionStatus(Enum):
    PENDING = "pending"
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class Position:
    def __init__(self, trade_signal: Dict):
        self.logger = logging.getLogger(__name__)
        
        # Basic position information
        self.symbol = trade_signal['symbol']
        self.strategy_type = trade_signal['strategy_type']
        self.direction = trade_signal['direction']
        self.position_size = trade_signal['position_size']
        
        # Price levels
        self.entry_price = trade_signal['entry_price']
        self.stop_loss = trade_signal['stop_loss']
        self.take_profit = trade_signal['take_profit']
        
        # Options specific data
        self.expiration = trade_signal['expiration']
        self.strikes = trade_signal['strike_selection']
        
        # Position tracking
        self.status = PositionStatus.PENDING
        self.entry_time: Optional[datetime] = None
        self.exit_time: Optional[datetime] = None
        self.exit_price: Optional[float] = None
        self.pnl: float = 0.0
        self.commission: float = 0.0
        
        # Risk management
        self.risk_amount = self._calculate_risk()
        self.risk_reward_ratio = self._calculate_risk_reward()
        
        # Position adjustments
        self.stop_loss_adjustments = []
        self.take_profit_adjustments = []
        
    def open_position(self, fill_price: float, timestamp: datetime):
        """Record position opening"""
        try:
            self.entry_price = fill_price
            self.entry_time = timestamp
            self.status = PositionStatus.OPEN
            self.logger.info(f"Opened position for {self.symbol} at {fill_price}")
        except Exception as e:
            self.logger.error(f"Error opening position: {str(e)}")
            
    def close_position(self, fill_price: float, timestamp: datetime):
        """Record position closing"""
        try:
            self.exit_price = fill_price
            self.exit_time = timestamp
            self.status = PositionStatus.CLOSED
            self._calculate_pnl()
            self.logger.info(f"Closed position for {self.symbol} at {fill_price}. PnL: {self.pnl}")
        except Exception as e:
            self.logger.error(f"Error closing position: {str(e)}")
            
    def adjust_stop_loss(self, new_stop_loss: float, timestamp: datetime):
        """Adjust stop loss level"""
        try:
            self.stop_loss_adjustments.append({
                'old_level': self.stop_loss,
                'new_level': new_stop_loss,
                'timestamp': timestamp
            })
            self.stop_loss = new_stop_loss
            self.logger.info(f"Adjusted stop loss for {self.symbol} to {new_stop_loss}")
        except Exception as e:
            self.logger.error(f"Error adjusting stop loss: {str(e)}")
            
    def adjust_take_profit(self, new_take_profit: float, timestamp: datetime):
        """Adjust take profit level"""
        try:
            self.take_profit_adjustments.append({
                'old_level': self.take_profit,
                'new_level': new_take_profit,
                'timestamp': timestamp
            })
            self.take_profit = new_take_profit
            self.logger.info(f"Adjusted take profit for {self.symbol} to {new_take_profit}")
        except Exception as e:
            self.logger.error(f"Error adjusting take profit: {str(e)}")
            
    def should_close(self, current_price: float) -> bool:
        """Check if position should be closed based on current price"""
        if self.status != PositionStatus.OPEN:
            return False
            
        # Check stop loss
        if self.direction == 'long' and current_price <= self.stop_loss:
            return True
        if self.direction == 'short' and current_price >= self.stop_loss:
            return True
            
        # Check take profit
        if self.direction == 'long' and current_price >= self.take_profit:
            return True
        if self.direction == 'short' and current_price <= self.take_profit:
            return True
            
        return False
        
    def get_current_pnl(self, current_price: float) -> float:
        """Calculate current unrealized PnL"""
        if self.status != PositionStatus.OPEN:
            return self.pnl
            
        price_diff = current_price - self.entry_price
        if self.direction == 'short':
            price_diff = -price_diff
            
        return (price_diff * self.position_size) - self.commission
        
    def to_dict(self) -> Dict:
        """Convert position to dictionary format"""
        return {
            'symbol': self.symbol,
            'strategy_type': self.strategy_type,
            'direction': self.direction,
            'position_size': self.position_size,
            'entry_price': self.entry_price,
            'stop_loss': self.stop_loss,
            'take_profit': self.take_profit,
            'expiration': self.expiration,
            'strikes': self.strikes,
            'status': self.status.value,
            'entry_time': self.entry_time.isoformat() if self.entry_time else None,
            'exit_time': self.exit_time.isoformat() if self.exit_time else None,
            'exit_price': self.exit_price,
            'pnl': self.pnl,
            'commission': self.commission,
            'risk_amount': self.risk_amount,
            'risk_reward_ratio': self.risk_reward_ratio
        }
        
    def _calculate_pnl(self):
        """Calculate realized PnL after position is closed"""
        if self.status != PositionStatus.CLOSED:
            return
            
        price_diff = self.exit_price - self.entry_price
        if self.direction == 'short':
            price_diff = -price_diff
            
        self.pnl = (price_diff * self.position_size) - self.commission
        
    def _calculate_risk(self) -> float:
        """Calculate risk amount for the position"""
        risk_per_unit = abs(self.entry_price - self.stop_loss)
        return risk_per_unit * self.position_size
        
    def _calculate_risk_reward(self) -> float:
        """Calculate risk/reward ratio"""
        risk = abs(self.entry_price - self.stop_loss)
        reward = abs(self.take_profit - self.entry_price)
        return reward / risk if risk != 0 else 0