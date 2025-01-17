from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Array
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    content = Column(Text)
    url = Column(String(1000))
    source = Column(String(200))
    published_date = Column(DateTime)
    keywords = Column(Array(String))
    created_at = Column(DateTime, default=datetime.utcnow)

class Summary(Base):
    __tablename__ = 'summaries'
    
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    summary_text = Column(Text)
    model_used = Column(String(100))
    keywords = Column(Array(String))
    created_at = Column(DateTime, default=datetime.utcnow)

class UserFeedback(Base):
    __tablename__ = 'user_feedback'
    
    id = Column(Integer, primary_key=True)
    summary_id = Column(Integer, ForeignKey('summaries.id'))
    feedback_type = Column(String(50))  # downvote, irrelevant, poor_summary
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow) 