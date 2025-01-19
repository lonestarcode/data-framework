from ...base.interfaces.trainer_interface import TrainerInterface
from ...data_manager import MLDataManager
from typing import Dict, Any

class BaseTrainer(TrainerInterface):
    def __init__(self, config: dict):
        self.config = config
        self.data_manager = MLDataManager()
        self.model = None
        
    async def prepare_data(self) -> tuple:
        """Fetch and prepare training data"""
        raw_data = await self.data_manager.fetch_training_data(
            data_type=self.config['data_type'],
            time_range=self.config['time_range']
        )
        return self._process_raw_data(raw_data)
    
    def _process_raw_data(self, raw_data: Dict) -> tuple:
        """Process raw data into training format"""
        raise NotImplementedError
        
    async def save_metrics(self, metrics: Dict[str, Any]) -> None:
        """Save training metrics"""
        await self.data_manager.store_model_results({
            'type': 'metrics',
            'data': metrics
        }) 