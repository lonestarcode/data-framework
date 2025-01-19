from typing import Dict, Any, Optional, List
from .database.mongo_manager import MongoManager
from .database.sql_manager import SQLManager
from .models.base import RawData, ProcessedData, ValidatedData
from datetime import datetime
import logging

class GlobalDataManager:
    def __init__(self, mongo_uri: str, sql_uri: str):
        self.mongo = MongoManager(mongo_uri)
        self.sql = SQLManager(sql_uri)
        self.logger = logging.getLogger(__name__)
    
    async def store_raw_data(self, source: str, data_type: str, 
                            content: Dict[str, Any], 
                            metadata: Optional[Dict] = None) -> str:
        """Store raw data from applications"""
        raw_data = RawData(
            source=source,
            data_type=data_type,
            content=content,
            metadata=metadata or {}
        )
        return await self.mongo.store_raw_data(raw_data)
    
    async def get_data_for_processing(self, data_type: str, 
                                    filters: Optional[Dict] = None) -> List[Dict]:
        """Get raw data ready for processing"""
        query = filters or {}
        query["processed"] = {"$ne": True}
        return await self.mongo.get_raw_data(data_type, query)
    
    async def mark_as_processed(self, data_type: str, data_id: str, 
                              processed_id: str) -> bool:
        """Mark raw data as processed"""
        return await self.mongo.update_raw_data(
            data_type, 
            data_id,
            {
                "processed": True,
                "processed_id": processed_id,
                "processed_at": datetime.now()
            }
        )
