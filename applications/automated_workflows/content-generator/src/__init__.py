from pathlib import Path
import logging
import yaml

# Setup package-level logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Load config
CONFIG_PATH = Path(__file__).parent.parent / 'config' / 'generator_config.yaml'

def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

config = load_config() 