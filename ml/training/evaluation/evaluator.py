from typing import Dict, Any, List
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from ...data_manager import MLDataManager

class ModelEvaluator:
    def __init__(self, model, data_manager: MLDataManager):
        self.model = model
        self.data_manager = data_manager
        
    async def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Evaluate model performance"""
        predictions = self.model.predict(X_test)
        metrics = self._calculate_metrics(y_test, predictions)
        await self._save_metrics(metrics)
        return metrics
        
    def _calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """Calculate standard metrics"""
        return {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'f1': f1_score(y_true, y_pred, average='weighted')
        }
        
    async def _save_metrics(self, metrics: Dict[str, float]) -> None:
        """Save metrics to database"""
        await self.data_manager.store_model_results({
            'type': 'metrics',
            'model_info': self.model.get_model_info(),
            'data': metrics
        }) 