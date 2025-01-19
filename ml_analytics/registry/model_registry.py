from typing import Dict, Any, Optional, List
import yaml
import json
from datetime import datetime
from pathlib import Path
from .versioning.version_control import VersionControl
from .initial_training.initial_trainer import InitialModelTrainer

class ModelRegistry:
    def __init__(self):
        self.registry_path = Path("ml_analytics/registry")
        self.metadata_path = self.registry_path / "metadata"
        self.versioning = VersionControl(self.registry_path)
        self.initial_trainer = InitialModelTrainer()
        self._initialize_registry()

    def _initialize_registry(self):
        """Initialize registry directory structure"""
        self.metadata_path.mkdir(parents=True, exist_ok=True)

    def register_model(self, model_name: str, model: Any, version: str) -> str:
        """Register a new model or version"""
        model_id = f"{model_name}-{version}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        metadata = {
            "model_id": model_id,
            "name": model_name,
            "version": version,
            "created_at": datetime.now().isoformat(),
            "status": "registered",
            "metadata": model.metadata if hasattr(model, 'metadata') else {}
        }

        # Save metadata
        with open(self.metadata_path / f"{model_id}.json", 'w') as f:
            json.dump(metadata, f, indent=2)

        # Create initial version
        self.versioning.create_version(model_id, {
            "metadata": metadata,
            "changes": ["Initial model registration"]
        })

        return model_id

    def get_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve model metadata"""
        metadata_file = self.metadata_path / f"{model_id}.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                return json.load(f)
        return None

    def update_model_status(self, model_id: str, status: str) -> None:
        """Update model status"""
        metadata = self.get_model(model_id)
        if metadata:
            metadata["status"] = status
            metadata["updated_at"] = datetime.now().isoformat()
            
            with open(self.metadata_path / f"{model_id}.json", 'w') as f:
                json.dump(metadata, f, indent=2)

    def get_model_versions(self, model_id: str) -> List[Dict[str, Any]]:
        """Get version history for model"""
        return self.versioning.get_version_history(model_id) 