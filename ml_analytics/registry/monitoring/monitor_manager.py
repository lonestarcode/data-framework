from typing import Dict, Any, List
from pathlib import Path
import json
from datetime import datetime
import numpy as np

class MonitorManager:
    def __init__(self, registry_path: Path):
        self.monitoring_path = registry_path / "monitoring"
        self.monitoring_path.mkdir(parents=True, exist_ok=True)
        
    async def track_model_performance(self, model_id: str, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Track model performance metrics"""
        performance_data = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "resource_usage": self._get_resource_usage()
        }
        
        model_monitoring_path = self.monitoring_path / model_id
        model_monitoring_path.mkdir(exist_ok=True)
        
        with open(model_monitoring_path / f"performance_{datetime.now().strftime('%Y%m%d%H%M%S')}.json", 'w') as f:
            json.dump(performance_data, f, indent=2)
            
        return self._check_drift(model_id, metrics)
        
    def _check_drift(self, model_id: str, current_metrics: Dict[str, float]) -> Dict[str, Any]:
        """Check for model drift"""
        history = self._get_metrics_history(model_id)
        if not history:
            return {"drift_detected": False}
            
        drift_results = {}
        for metric, value in current_metrics.items():
            historical_values = [h["metrics"].get(metric, 0) for h in history]
            drift_results[metric] = {
                "current": value,
                "mean": np.mean(historical_values),
                "std": np.std(historical_values),
                "drift_detected": abs(value - np.mean(historical_values)) > 2 * np.std(historical_values)
            }
            
        return {
            "drift_detected": any(m["drift_detected"] for m in drift_results.values()),
            "metrics_drift": drift_results
        } 