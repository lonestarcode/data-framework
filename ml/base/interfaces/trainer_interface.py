from abc import ABC, abstractmethod
from typing import Dict, Any

class TrainerInterface(ABC):
    @abstractmethod
    def prepare_data(self) -> tuple:
        """Prepare training data"""
        pass
    
    @abstractmethod
    def train(self) -> None:
        """Execute training process"""
        pass
    
    @abstractmethod
    def evaluate(self) -> Dict[str, Any]:
        """Evaluate model performance"""
        pass 