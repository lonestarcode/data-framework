class BaseModelTrainer:
    def __init__(self):
        self.data_manager = MLDataManager()
        
    async def prepare_training_data(self):
        # Get validated data from global database
        raw_data = await self.data_manager.fetch_training_data(
            data_type=self.config.data_type,
            time_range=self.config.time_range
        )
        
        # Process for training
        return self.preprocessor.transform(raw_data)
    
    async def save_model_metrics(self, metrics: dict):
        # Store structured metrics in SQL
        await self.data_manager.store_model_results({
            'type': 'metrics',
            'data': metrics
        }) 