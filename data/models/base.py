from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class BaseData(BaseModel):
    id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class RawData(BaseData):
    source: str
    data_type: str
    content: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ProcessedData(BaseData):
    source_id: str
    data_type: str
    content: Dict[str, Any]
    features: Dict[str, Any]
    validation_status: str = "pending"
    processing_metadata: Dict[str, Any] = Field(default_factory=dict)

class ValidatedData(ProcessedData):
    validation_score: float
    validated_by: str
    validation_date: datetime = Field(default_factory=datetime.now)
