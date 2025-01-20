from typing import Dict, Any, Optional
import argparse
import json
import sys
from ml_analytics.registry.model_registry import ModelRegistry

class TrainingPipeline:
    def __init__(self):
        self.registry = ModelRegistry()
        
    async def execute_training(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute training pipeline when called by Spring Boot"""
        experiment_id = await self.registry.create_experiment(
            name=config["name"],
            config=config
        )
        
        try:
            model_id = await self.registry.initial_trainer.train_initial_model(
                model=config["model"],
                data=config["data"]
            )
            
            await self._handle_post_training(model_id, config)
            
            # Return JSON format for Spring Boot
            return json.dumps({
                "status": "success",
                "model_id": model_id,
                "experiment_id": experiment_id
            })
            
        except Exception as e:
            await self.registry.experiment_manager.log_result(
                experiment_id, 
                {"status": "failed", "error": str(e)}
            )
            return json.dumps({
                "status": "error",
                "error": str(e)
            })

if __name__ == "__main__":
    # Parse arguments from Spring Boot
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    args = parser.parse_args()
    
    # Execute pipeline
    config = json.loads(args.config)
    pipeline = TrainingPipeline()
    result = pipeline.execute_training(config)
    
    # Output JSON for Spring Boot to parse
    print(result)
    sys.exit(0)

    async def _handle_post_training(self, model_id: str, config: Dict[str, Any]) -> None:
        """Handle post-training tasks"""
        await self.registry.governance_manager.register_model_governance(
            model_id, config.get("governance_data", {})
        )
        await self.registry.monitor_manager.track_model_performance(
            model_id, config.get("metrics", {})
        ) 