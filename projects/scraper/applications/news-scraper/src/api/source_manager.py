from typing import List, Dict
from sqlalchemy.orm import Session
from datetime import datetime

class SourceManager:
    def __init__(self, db_session: Session):
        self.db = db_session
        
    def add_source(self, source_data: Dict) -> Dict:
        new_source = NewsSource(
            name=source_data["name"],
            url=source_data["url"],
            type=source_data["type"],
            scraping_interval=source_data.get("interval", "1h"),
            added_by_user=True,
            created_at=datetime.utcnow()
        )
        
        try:
            self.db.add(new_source)
            self.db.commit()
            return {"status": "success", "source_id": new_source.id}
        except Exception as e:
            self.db.rollback()
            return {"status": "error", "message": str(e)}
    
    def get_sources(self, source_type: str = None) -> List[Dict]:
        query = self.db.query(NewsSource)
        if source_type:
            query = query.filter(NewsSource.type == source_type)
        return [source.to_dict() for source in query.all()] 