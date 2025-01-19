from typing import Dict, Any
import logging
from datetime import datetime
from ...data_manager import MLDataManager

class PerformanceMonitor:
    def __init__(self, model_info: Dict[str, Any], data_manager: MLDataManager):
        self.model_info = model_info
        self.data_manager = data_manager
        self.logger = logging.getLogger(__name__)
        
    async def log_training_metrics(self, metrics: Dict[str, float], step: int) -> None:
        """Log training metrics"""
        await self.data_manager.store_model_results({
            'type': 'training_metrics',
            'model_info': self.model_info,
            'step': step,
            'timestamp': datetime.now(),
            'data': metrics
        })
        
    async def log_prediction_metrics(self, metrics: Dict[str, float]) -> None:
        """Log prediction performance metrics"""
        await self.data_manager.store_model_results({
            'type': 'prediction_metrics',
            'model_info': self.model_info,
            'timestamp': datetime.now(),
            'data': metrics
        })
        
    async def log_resource_usage(self, usage_metrics: Dict[str, float]) -> None:
        """Log resource utilization"""
        await self.data_manager.store_model_results({
            'type': 'resource_metrics',
            'model_info': self.model_info,
            'timestamp': datetime.now(),
            'data': usage_metrics
        }) 