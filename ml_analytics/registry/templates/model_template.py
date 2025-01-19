from typing import Dict, Any
from ml_analytics.models.base.model_base import BaseModel

class ModelTemplate(BaseModel):
    def __init__(self, model_type: str, config: Dict[str, Any]):
        super().__init__()
        self.model_type = model_type
        self.config = config
        self.model = None
        
    def initialize_model(self):
        """Initialize model based on type and config"""
        if self.model_type == "nlp":
            self._init_nlp_model()
        elif self.model_type == "market":
            self._init_market_model()
        elif self.model_type == "vision":
            self._init_vision_model()
            
    def _init_nlp_model(self):
        self.metadata.update({
            "type": "nlp",
            "architecture": self.config.get("architecture", "transformer"),
            "vocab_size": self.config.get("vocab_size", 30000)
        })
        
    def _init_market_model(self):
        self.metadata.update({
            "type": "market",
            "architecture": self.config.get("architecture", "lstm"),
            "sequence_length": self.config.get("sequence_length", 60)
        })
        
    def _init_vision_model(self):
        self.metadata.update({
            "type": "vision",
            "architecture": self.config.get("architecture", "cnn"),
            "input_shape": self.config.get("input_shape", [224, 224, 3])
        }) 