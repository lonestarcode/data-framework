from pymongo import MongoClient
from sqlalchemy import create_engine
from config import settings

class MLDataManager:
    def __init__(self):
        self.mongo_client = MongoClient(settings.MONGODB_URI)
        self.sql_engine = create_engine(settings.SQL_URI)
        
    async def fetch_training_data(self, data_type: str, time_range: dict):
        """Fetch training data from both databases based on type"""
        if data_type in ['text', 'social', 'raw_market']:
            # Fetch unstructured data from MongoDB
            return await self._fetch_mongo_data(data_type, time_range)
        else:
            # Fetch structured data from SQL
            return await self._fetch_sql_data(data_type, time_range)
    
    async def store_model_results(self, results: dict):
        """Store model outputs in appropriate database"""
        if results['type'] in ['predictions', 'embeddings']:
            # Store flexible outputs in MongoDB
            await self._store_mongo_results(results)
        else:
            # Store structured metrics in SQL
            await self._store_sql_results(results) 