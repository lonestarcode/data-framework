import asyncio
from fastapi import FastAPI
from src.api import app
from src.pipeline.data_pipeline import MarketplacePipeline
from src.logging.logger import get_logger
from src.monitoring.metrics import SCRAPE_COUNTER

logger = get_logger(__name__)

async def scrape_categories():
    """Background task to scrape marketplace categories"""
    pipeline = MarketplacePipeline()
    categories = ["bikes", "electronics", "furniture"]
    
    while True:
        for category in categories:
            try:
                await pipeline.process_category(category)
                SCRAPE_COUNTER.labels(category=category).inc()
            except Exception as e:
                logger.error(f"Error processing category {category}: {str(e)}")
        await asyncio.sleep(300)  # 5 minutes between scrapes

@app.on_event("startup")
async def startup_event():
    """Start background scraping task on application startup"""
    asyncio.create_task(scrape_categories())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
