from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict, Any, List
from ..models.base import RawData
import logging

class MongoManager:
    def __init__(self, uri: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client.global_data
        self.logger = logging.getLogger(__name__)
    
    async def store_raw_data(self, data: RawData) -> str:
        """Store raw data in appropriate collection"""
        collection = self.db[f"raw_{data.data_type}"]
        result = await collection.insert_one(data.dict())
        return str(result.inserted_id)
    
    async def get_raw_data(self, data_type: str, query: Dict[str, Any]) -> List[Dict]:
        """Retrieve raw data for processing"""
        collection = self.db[f"raw_{data_type}"]
        cursor = collection.find(query)
        return await cursor.to_list(length=None)
    
    async def update_raw_data(self, data_type: str, data_id: str, 
                            updates: Dict[str, Any]) -> bool:
        """Update raw data document"""
        collection = self.db[f"raw_{data_type}"]
        result = await collection.update_one(
            {"_id": data_id},
            {"$set": updates}
        )
        return result.modified_count > 0
