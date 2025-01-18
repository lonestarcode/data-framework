from typing import Dict, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
import logging
from dataclasses import dataclass

@dataclass
class OptionChain:
    calls: pd.DataFrame
    puts: pd.DataFrame
    underlying_price: float
    timestamp: datetime

class MarketData:
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)  # Cache data for 5 minutes
        
    async def get_market_snapshot(self, symbol: str) -> Dict:
        """Get current market snapshot for a symbol"""
        try:
            # Check cache first
            if self._is_cache_valid(symbol):
                return self.cache[symbol]['data']
                
            # Fetch new data
            stock = yf.Ticker(symbol)
            info = stock.info
            
            snapshot = {
                'symbol': symbol,
                'price': info.get('regularMarketPrice'),
                'volume': info.get('volume'),
                'timestamp': datetime.now(),
                'bid': info.get('bid'),
                'ask': info.get('ask'),
                'day_high': info.get('dayHigh'),
                'day_low': info.get('dayLow'),
                'fifty_day_avg': info.get('fiftyDayAverage'),
                'two_hundred_day_avg': info.get('twoHundredDayAverage'),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('forwardPE'),
                'sector': info.get('sector'),
                'industry': info.get('industry')
            }
            
            # Update cache
            self._update_cache(symbol, snapshot)
            
            return snapshot
            
        except Exception as e:
            self.logger.error(f"Error fetching market snapshot for {symbol}: {str(e)}")
            raise
            
    async def get_option_chain(self, symbol: str) -> Optional[OptionChain]:
        """Get option chain data for a symbol"""
        try:
            stock = yf.Ticker(symbol)
            options = stock.options
            
            if not options:
                self.logger.warning(f"No options available for {symbol}")
                return None
                
            # Get the nearest expiration date
            nearest_expiry = options[0]
            chain = stock.option_chain(nearest_expiry)
            
            return OptionChain(
                calls=chain.calls,
                puts=chain.puts,
                underlying_price=stock.info['regularMarketPrice'],
                timestamp=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Error fetching option chain for {symbol}: {str(e)}")
            return None
            
    async def get_technical_indicators(self, symbol: str) -> Dict:
        """Calculate technical indicators for a symbol"""
        try:
            # Get historical data
            stock = yf.Ticker(symbol)
            hist = stock.history(period='6mo')
            
            indicators = {
                'rsi': self._calculate_rsi(hist['Close']),
                'macd': self._calculate_macd(hist['Close']),
                'bollinger_bands': self._calculate_bollinger_bands(hist['Close']),
                'volume_sma': self._calculate_volume_sma(hist['Volume']),
                'atr': self._calculate_atr(hist),
                'timestamp': datetime.now()
            }
            
            return indicators
            
        except Exception as e:
            self.logger.error(f"Error calculating technical indicators for {symbol}: {str(e)}")
            raise
            
    async def get_volatility_metrics(self, symbol: str) -> Dict:
        """Calculate volatility metrics for a symbol"""
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(period='1y')
            
            # Calculate historical volatility
            returns = np.log(hist['Close'] / hist['Close'].shift(1))
            hist_vol = returns.std() * np.sqrt(252)  # Annualized
            
            # Get implied volatility if available
            option_chain = await self.get_option_chain(symbol)
            if option_chain:
                atm_call = self._find_atm_option(option_chain.calls, option_chain.underlying_price)
                implied_vol = atm_call['impliedVolatility'] if atm_call is not None else None
            else:
                implied_vol = None
                
            metrics = {
                'historical_volatility': hist_vol,
                'implied_volatility': implied_vol,
                'iv_percentile': self._calculate_iv_percentile(symbol),
                'iv_rank': self._calculate_iv_rank(symbol),
                'timestamp': datetime.now()
            }
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error calculating volatility metrics for {symbol}: {str(e)}")
            raise
            
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """Calculate RSI technical indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs)).iloc[-1]
        
    def _calculate_macd(self, prices: pd.Series) -> Dict:
        """Calculate MACD indicator"""
        exp1 = prices.ewm(span=12, adjust=False).mean()
        exp2 = prices.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        
        return {
            'macd': macd.iloc[-1],
            'signal': signal.iloc[-1],
            'histogram': macd.iloc[-1] - signal.iloc[-1]
        }
        
    def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20) -> Dict:
        """Calculate Bollinger Bands"""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        
        return {
            'upper': sma.iloc[-1] + (std.iloc[-1] * 2),
            'middle': sma.iloc[-1],
            'lower': sma.iloc[-1] - (std.iloc[-1] * 2)
        }
        
    def _calculate_volume_sma(self, volume: pd.Series, period: int = 20) -> float:
        """Calculate volume SMA"""
        return volume.rolling(window=period).mean().iloc[-1]
        
    def _calculate_atr(self, data: pd.DataFrame, period: int = 14) -> float:
        """Calculate Average True Range"""
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(window=period).mean().iloc[-1]
        
    def _calculate_iv_percentile(self, symbol: str) -> Optional[float]:
        """Calculate IV percentile"""
        try:
            # This would typically use historical IV data
            # Placeholder implementation
            return 0.5
        except Exception:
            return None
            
    def _calculate_iv_rank(self, symbol: str) -> Optional[float]:
        """Calculate IV rank"""
        try:
            # This would typically use historical IV data
            # Placeholder implementation
            return 0.5
        except Exception:
            return None
            
    def _find_atm_option(self, options: pd.DataFrame, underlying_price: float) -> Optional[Dict]:
        """Find at-the-money option"""
        if options.empty:
            return None
            
        # Find the strike price closest to current price
        options['strike_diff'] = abs(options['strike'] - underlying_price)
        atm_option = options.loc[options['strike_diff'].idxmin()]
        
        return atm_option.to_dict()
        
    def _is_cache_valid(self, symbol: str) -> bool:
        """Check if cached data is still valid"""
        if symbol not in self.cache:
            return False
            
        age = datetime.now() - self.cache[symbol]['timestamp']
        return age < self.cache_duration
        
    def _update_cache(self, symbol: str, data: Dict):
        """Update cache with new data"""
        self.cache[symbol] = {
            'data': data,
            'timestamp': datetime.now()
        }