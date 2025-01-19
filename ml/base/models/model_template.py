from typing import Any, Dict, Optional, Union
import numpy as np
from datetime import datetime
from ...data_manager import MLDataManager
from ..interfaces.model_interface import ModelInterface

class ModelTemplate(ModelInterface):
    """Template for creating ML models with standardized data handling"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = None
        self.data_manager = MLDataManager()
        self.model_info = {
            'name': config.get('name', 'unnamed_model'),
            'version': config.get('version', '0.1'),
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'metadata': config.get('metadata', {})
        }
    
    async def load_training_data(self, data_config: Dict[str, Any]) -> tuple:
        """Load and prepare training data"""
        raw_data = await self.data_manager.fetch_training_data(
            data_type=data_config['data_type'],
            time_range=data_config.get('time_range', {})
        )
        return self._preprocess_data(raw_data)
    
    def _preprocess_data(self, raw_data: Any) -> tuple:
        """Preprocess raw data into format suitable for training"""
        raise NotImplementedError("Implement preprocessing logic in child class")
    
    async def save_predictions(self, predictions: Union[np.ndarray, Dict], 
                             metadata: Optional[Dict] = None) -> None:
        """Save model predictions to appropriate database"""
        await self.data_manager.store_model_results({
            'type': 'predictions',
            'model_info': self.model_info,
            'data': predictions,
            'metadata': metadata or {}
        })
    
    async def log_metrics(self, metrics: Dict[str, Any]) -> None:
        """Log model metrics to SQL database"""
        await self.data_manager.store_model_results({
            'type': 'metrics',
            'model_info': self.model_info,
            'data': metrics
        })
    
    def validate_config(self) -> bool:
        """Validate model configuration"""
        required_fields = ['name', 'version', 'data_type']
        return all(field in self.config for field in required_fields)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get current model information"""
        return {
            **self.model_info,
            'config': self.config,
            'updated_at': datetime.now()
        }
    
    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Train model implementation"""
        raise NotImplementedError("Implement training logic in child class")
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Model prediction implementation"""
        raise NotImplementedError("Implement prediction logic in child class")
    
    def save(self, path: str) -> None:
        """Save model implementation"""
        raise NotImplementedError("Implement save logic in child class")
    
    def load(self, path: str) -> None:
        """Load model implementation"""
        raise NotImplementedError("Implement load logic in child class")
