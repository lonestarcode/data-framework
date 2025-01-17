from abc import ABC, abstractmethod
from typing import Dict, List

class BaseBroker(ABC):
    @abstractmethod
    async def connect(self):
        """Establish connection to broker API"""
        pass
    
    @abstractmethod
    async def disconnect(self):
        """Close broker connection"""
        pass
    
    @abstractmethod
    async def get_market_data(self) -> Dict:
        """Fetch current market data"""
        pass
    
    @abstractmethod
    async def get_option_chain(self, symbol: str) -> Dict:
        """Fetch option chain for given symbol"""
        pass
    
    @abstractmethod
    async def execute_trade(self, signal: Dict) -> bool:
        """Execute a trade based on signal"""
        pass
    
    @abstractmethod
    async def get_positions(self) -> List[Dict]:
        """Get current positions"""
        pass