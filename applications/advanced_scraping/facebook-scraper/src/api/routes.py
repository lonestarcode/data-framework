from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db_session
from src.database.models import MarketplaceListing, ListingAnalysis
from typing import List, Optional
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/listings/")
async def get_listings(
    category: Optional[str] = None,
    hours: Optional[int] = 24,
    session: AsyncSession = Depends(get_db_session)
):
    """Get marketplace listings with optional filtering"""
    try:
        query = session.query(MarketplaceListing)
        
        if category:
            query = query.filter(MarketplaceListing.category == category)
            
        if hours:
            time_threshold = datetime.utcnow() - timedelta(hours=hours)
            query = query.filter(MarketplaceListing.created_at >= time_threshold)
            
        return await query.all()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/listings/{listing_id}/analysis")
async def get_listing_analysis(
    listing_id: int,
    session: AsyncSession = Depends(get_db_session)
):
    """Get analysis for a specific listing"""
    try:
        analysis = await session.query(ListingAnalysis)\
            .filter(ListingAnalysis.listing_id == listing_id)\
            .first()
            
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
            
        return analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
