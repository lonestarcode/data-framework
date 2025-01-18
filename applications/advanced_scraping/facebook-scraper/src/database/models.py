from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class MarketplaceListing(Base):
    __tablename__ = 'marketplace_listings'
    
    id = Column(Integer, primary_key=True)
    listing_id = Column(String(100), unique=True)
    title = Column(String(500))
    price = Column(Float)
    description = Column(Text)
    location = Column(String(200))
    category = Column(String(100))
    seller_id = Column(String(100))
    listing_url = Column(String(1000))
    images = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

class ListingAnalysis(Base):
    __tablename__ = 'listing_analyses'
    
    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('marketplace_listings.id'))
    quality_score = Column(Float)
    keywords = Column(JSON)
    category_confidence = Column(Float)
    analyzed_at = Column(DateTime, default=datetime.utcnow)