from ..interfaces.model_interface import ModelInterface
import numpy as np
import joblib

class BaseModel(ModelInterface):
    def __init__(self, model_config: dict):
        self.config = model_config
        self.model = None
        
    def save(self, path: str) -> None:
        """Save model to disk"""
        if self.model is not None:
            joblib.dump(self.model, path)
            
    def load(self, path: str) -> None:
        """Load model from disk"""
        self.model = joblib.load(path) 