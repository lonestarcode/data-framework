import asyncio
import logging
from pathlib import Path
import yaml
from dotenv import load_dotenv

from broker.tdameritrade import TDAmeritrade
from analysis.gpt_analyzer import GPTAnalyzer
from trading.strategy import OptionsStrategy
from utils.logger import setup_logger

async def main():
    # Load configuration
    config_path = Path("config/config.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Setup logging
    setup_logger()
    logger = logging.getLogger(__name__)
    
    # Initialize components
    broker = TDAmeritrade(config["broker"])
    analyzer = GPTAnalyzer(config["gpt"])
    strategy = OptionsStrategy(config["trading"])
    
    try:
        await broker.connect()
        logger.info("Starting trading bot...")
        
        while True:
            # Get market data
            market_data = await broker.get_market_data()
            
            # Analyze market conditions
            analysis = await analyzer.analyze_market_conditions(market_data)
            
            # Generate trading signals
            signals = strategy.generate_trade_signals(analysis, market_data)
            
            # Execute trades
            for signal in signals:
                await broker.execute_trade(signal)
            
            # Wait for next iteration
            await asyncio.sleep(60)  # 1-minute cycle
            
    except Exception as e:
        logger.error(f"Error in main loop: {str(e)}")
        raise
    finally:
        await broker.disconnect()

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())