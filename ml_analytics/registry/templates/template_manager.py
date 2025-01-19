from typing import Dict, Any, Optional
import yaml
from pathlib import Path

class TemplateManager:
    def __init__(self, registry_path: Path):
        self.templates_path = registry_path / "templates"
        self.templates_path.mkdir(parents=True, exist_ok=True)
        self.registry_config = self._load_registry_config()
        
    def _load_registry_config(self) -> Dict[str, Any]:
        with open(Path("ml_analytics/registry/registry.yaml"), 'r') as f:
            config = yaml.safe_load(f)
            return config["model_registry"]["templates"]
            
    def get_template_config(self, model_type: str) -> Optional[Dict[str, Any]]:
        """Get configuration for specific model type"""
        return self.registry_config.get(model_type)
        
    def create_template(self, model_type: str, custom_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create new template with custom configuration"""
        base_config = self.get_template_config(model_type) or {}
        template_config = {**base_config, **custom_config}
        
        template_file = self.templates_path / f"{model_type}_template.yaml"
        with open(template_file, 'w') as f:
            yaml.dump(template_config, f)
            
        return template_config 