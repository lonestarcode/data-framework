from typing import Dict, Any, Optional
from datetime import datetime
import json
import os
from ...config import settings

class ModelRegistry:
    def __init__(self):
        self.registry_path = settings.MODEL_DIR / 'registry'
        self.registry_path.mkdir(parents=True, exist_ok=True)
        self._load_registry()
        
    def _load_registry(self):
        """Load existing registry from disk"""
        registry_file = self.registry_path / 'registry.json'
        if registry_file.exists():
            with open(registry_file, 'r') as f:
                self.registry = json.load(f)
        else:
            self.registry = {}
            
    def _save_registry(self):
        """Save registry to disk"""
        with open(self.registry_path / 'registry.json', 'w') as f:
            json.dump(self.registry, f, indent=2, default=str)
            
    def register_model(self, name: str, model: Any, version: str,
                      metadata: Optional[Dict] = None) -> None:
        """Register a model with version control"""
        if name not in self.registry:
            self.registry[name] = {}
            
        self.registry[name][version] = {
            'registered_at': datetime.now(),
            'path': f'models/{name}/{version}',
            'metadata': metadata or {}
        }
        
        # Save model
        model_path = self.registry_path / f'models/{name}/{version}'
        model_path.mkdir(parents=True, exist_ok=True)
        model.save(str(model_path / 'model.pkl'))
        self._save_registry()
        
    def get_model(self, name: str, version: Optional[str] = None) -> Any:
        """Retrieve a model by name and version"""
        if name not in self.registry:
            raise KeyError(f"Model {name} not found in registry")
            
        if version is None:
            # Get latest version
            version = max(self.registry[name].keys())
            
        if version not in self.registry[name]:
            raise KeyError(f"Version {version} not found for model {name}")
            
        model_path = self.registry_path / self.registry[name][version]['path'] / 'model.pkl'
        return ModelTemplate.load(str(model_path))
        
    def list_models(self) -> Dict[str, Any]:
        """List all registered models and versions"""
        return self.registry
        
    def get_model_info(self, name: str, version: Optional[str] = None) -> Dict[str, Any]:
        """Get model metadata"""
        if name not in self.registry:
            raise KeyError(f"Model {name} not found in registry")
            
        if version is None:
            return self.registry[name]
        
        if version not in self.registry[name]:
            raise KeyError(f"Version {version} not found for model {name}")
            
        return self.registry[name][version] 