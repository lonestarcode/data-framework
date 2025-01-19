from typing import Dict, Any, Optional, List
import yaml
import json
from datetime import datetime
from pathlib import Path
from .versioning.version_control import VersionControl
from .metadata.metadata_manager import MetadataManager
from .templates.template_manager import TemplateManager
from .initial_training.initial_trainer import InitialModelTrainer
from .monitoring.monitor_manager import MonitorManager
from .governance.governance_manager import GovernanceManager
from .lineage.lineage_tracker import LineageTracker
from .experiments.experiment_manager import ExperimentManager

class ModelRegistry:
    def __init__(self):
        self.registry_path = Path("ml_analytics/registry")
        self.versioning = VersionControl(self.registry_path)
        self.metadata_manager = MetadataManager(self.registry_path)
        self.template_manager = TemplateManager(self.registry_path)
        self.initial_trainer = InitialModelTrainer()
        self.monitor_manager = MonitorManager(self.registry_path)
        self.governance_manager = GovernanceManager(self.registry_path)
        self.lineage_tracker = LineageTracker(self.registry_path)
        self.experiment_manager = ExperimentManager(self.registry_path)

    async def register_model(self, model_name: str, model: Any, version: str) -> str:
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
        self.metadata_manager.save_metadata(model_id, metadata)
        
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

    async def track_model_performance(self, model_id: str, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Track model performance and check for drift"""
        return await self.monitor_manager.track_model_performance(model_id, metrics)

    async def register_governance(self, model_id: str, governance_data: Dict[str, Any]) -> None:
        """Register model governance information"""
        await self.governance_manager.register_model_governance(model_id, governance_data)

    async def track_lineage(self, model_id: str, parent_id: Optional[str], metadata: Dict[str, Any]) -> None:
        """Track model lineage"""
        self.lineage_tracker.track_model_lineage(model_id, parent_id, metadata)

    async def create_experiment(self, name: str, config: Dict[str, Any]) -> str:
        """Create new experiment"""
        return await self.experiment_manager.create_experiment(name, config) 