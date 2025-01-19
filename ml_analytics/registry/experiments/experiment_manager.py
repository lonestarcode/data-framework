from typing import Dict, Any, List, Optional
from pathlib import Path
import json
from datetime import datetime
import yaml

class ExperimentManager:
    def __init__(self, registry_path: Path):
        self.experiments_path = registry_path / "experiments"
        self.experiments_path.mkdir(parents=True, exist_ok=True)
        
    async def create_experiment(self, name: str, config: Dict[str, Any]) -> str:
        """Create new experiment"""
        experiment_id = f"{name}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        experiment_data = {
            "id": experiment_id,
            "name": name,
            "status": "created",
            "config": config,
            "created_at": datetime.now().isoformat(),
            "results": [],
            "artifacts": []
        }
        
        self._save_experiment(experiment_id, experiment_data)
        return experiment_id
        
    async def log_result(self, experiment_id: str, result: Dict[str, Any]) -> None:
        """Log experiment result"""
        experiment = self._load_experiment(experiment_id)
        if experiment:
            result["timestamp"] = datetime.now().isoformat()
            experiment["results"].append(result)
            self._save_experiment(experiment_id, experiment)
            
    def _save_experiment(self, experiment_id: str, data: Dict[str, Any]) -> None:
        with open(self.experiments_path / f"{experiment_id}.json", 'w') as f:
            json.dump(data, f, indent=2) 