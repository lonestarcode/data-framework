import os
from pathlib import Path

# Database settings
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
SQL_URI = os.getenv('SQL_URI', 'postgresql://user:pass@localhost:5432/mldb')

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent / 'data'
MODEL_DIR = BASE_DIR / 'models'

# Training settings
DEFAULT_BATCH_SIZE = 32
DEFAULT_EPOCHS = 10 