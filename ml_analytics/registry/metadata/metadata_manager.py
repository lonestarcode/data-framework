from typing import Dict, Any, Optional
from pathlib import Path
import json
from datetime import datetime

class MetadataManager:
    def __init__(self, registry_path: Path):
        self.metadata_path = registry_path / "metadata"
        self.metadata_path.mkdir(parents=True, exist_ok=True)
        
    def save_metadata(self, model_id: str, metadata: Dict[str, Any]) -> None:
        """Save or update model metadata"""
        metadata_file = self.metadata_path / f"{model_id}.json"
        
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                existing_metadata = json.load(f)
            existing_metadata.update(metadata)
            metadata = existing_metadata
            
        metadata["updated_at"] = datetime.now().isoformat()
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
            
    def get_metadata(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve model metadata"""
        metadata_file = self.metadata_path / f"{model_id}.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                return json.load(f)
        return None 