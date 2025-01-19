from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseModel(ABC):
    def __init__(self):
        self.metadata = {}
        self.version = "0.0.1"
        self.model_type = None

    @abstractmethod
    def train(self, data: Dict[str, Any]) -> None:
        """Train the model with provided data"""
        pass

    @abstractmethod
    def predict(self, input_data: Dict[str, Any]) -> Any:
        """Make predictions using the trained model"""
        pass

    @abstractmethod
    def evaluate(self, test_data: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate model performance"""
        pass

    def save_metadata(self, metadata: Dict[str, Any]) -> None:
        """Save model metadata"""
        self.metadata.update(metadata)
