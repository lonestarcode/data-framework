from typing import Dict, Any, Optional
from pathlib import Path
import yaml
from ml_analytics.models.base.model_base import BaseModel
from ml_analytics.registry.model_registry import ModelRegistry

class InitialModelTrainer:
    def __init__(self):
        self.registry = ModelRegistry()
        self.config_path = Path("ml_analytics/registry/initial_training/configs")
        self.training_config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        with open(self.config_path / "initial_training.yaml", "r") as f:
            return yaml.safe_load(f)
    
    async def train_initial_model(self, model: BaseModel, data: Dict[str, Any]) -> str:
        """Handle complete initial training process"""
        # Register initial model
        model_id = self.registry.register_model(
            model.__class__.__name__,
            model,
            version="0.0.1"
        )
        
        try:
            # Train model
            model.train(data)
            
            # Evaluate performance
            metrics = model.evaluate(data.get("validation_data", {}))
            
            if self._validate_metrics(metrics):
                # Update registry with successful training
                self.registry.update_model_status(
                    model_id, 
                    "trained",
                    metadata={
                        "metrics": metrics,
                        "training_completed": True
                    }
                )
                return model_id
            else:
                self.registry.update_model_status(model_id, "failed_validation")
                raise ValueError("Model failed validation criteria")
                
        except Exception as e:
            self.registry.update_model_status(model_id, "failed_training")
            raise
            
    def _validate_metrics(self, metrics: Dict[str, float]) -> bool:
        thresholds = self.training_config.get("validation", {}).get("thresholds", {})
        return all(
            metrics.get(metric, 0) >= threshold 
            for metric, threshold in thresholds.items()
        ) 