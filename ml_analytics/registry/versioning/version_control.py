from typing import Dict, Any, List
from pathlib import Path
import json
import shutil
from datetime import datetime

class VersionControl:
    def __init__(self, registry_path: Path):
        self.versioning_path = registry_path / "versioning"
        self.versioning_path.mkdir(parents=True, exist_ok=True)
        
    def create_version(self, model_id: str, model_data: Dict[str, Any]) -> str:
        """Create new version of model"""
        version_info = {
            "version_id": f"{model_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "parent_model": model_id,
            "created_at": datetime.now().isoformat(),
            "changes": model_data.get("changes", []),
            "metrics": model_data.get("metrics", {}),
            "metadata": model_data.get("metadata", {})
        }
        
        version_path = self.versioning_path / model_id
        version_path.mkdir(parents=True, exist_ok=True)
        
        with open(version_path / f"{version_info['version_id']}.json", 'w') as f:
            json.dump(version_info, f, indent=2)
            
        return version_info['version_id']
        
    def get_version_history(self, model_id: str) -> List[Dict[str, Any]]:
        """Get version history for model"""
        version_path = self.versioning_path / model_id
        if not version_path.exists():
            return []
            
        versions = []
        for version_file in version_path.glob("*.json"):
            with open(version_file, 'r') as f:
                versions.append(json.load(f))
                
        return sorted(versions, key=lambda x: x['created_at']) 