This trading bot combines artificial intelligence with traditional trading strategies to identify and execute options trading opportunities. It features:

- GPT-powered market analysis
- Real-time options data processing
- Risk management system
- Paper trading support
- Integration with TD Ameritrade API

## Quick Start

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run the bot:
```bash
python src/main.py
```

## Documentation

- [Installation Guide](docs/installation.md)
- [Configuration Guide](docs/configuration.md)
- [API Documentation](docs/api.md)
- [Trading Strategies](docs/trading_strategies.md)
- [Risk Management](docs/risk_management.md)
```

```markdown:docs/installation.md
# Installation Guide

## Prerequisites

- Python 3.8+
- TD Ameritrade Developer Account
- OpenAI API Key
- Git

## Step-by-Step Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/gpt-options-trader.git
cd gpt-options-trader
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment Variables**
Create a `.env` file in the root directory:
```env
TD_API_KEY=your_td_ameritrade_api_key
TD_ACCOUNT_ID=your_td_account_id
OPENAI_API_KEY=your_openai_api_key
```

5. **Configure Trading Parameters**
Edit `config/config.yaml` to set your trading parameters.

6. **Test Installation**
```bash
python -m pytest tests/
```

## Troubleshooting

### Common Issues

1. **TD Ameritrade API Connection Issues**
   - Verify API key is correct
   - Ensure redirect URI matches your application settings
   - Check if token.json is present and valid

2. **OpenAI API Issues**
   - Verify API key is correct
   - Check API usage limits
   - Ensure proper model access

3. **Dependencies Issues**
   - Try upgrading pip: `pip install --upgrade pip`
   - Install system dependencies if needed
```

```markdown:docs/configuration.md
# Configuration Guide

## Configuration Files

The bot uses two main configuration files:

1. `config/config.yaml` - Main configuration
2. `config/logging_config.yaml` - Logging configuration

## Main Configuration (config.yaml)

### Broker Settings
```yaml
broker:
  name: "tdameritrade"
  paper_trading: true
  api_key: ${TD_API_KEY}
  account_id: ${TD_ACCOUNT_ID}
  max_positions: 3
  max_loss_percent: 2.0
```

### Trading Parameters
```yaml
trading:
  max_position_size: 1000
  stop_loss_percent: 1.0
  take_profit_percent: 2.0
  max_trades_per_day: 5
  trading_hours:
    start: "09:30"
    end: "16:00"
```

### GPT Settings
```yaml
gpt:
  model: "gpt-4"
  api_key: ${OPENAI_API_KEY}
  temperature: 0.3
  max_tokens: 500
```

### Analysis Settings
```yaml
analysis:
  timeframe: "1d"
  indicators:
    - "IV_percentile"
    - "RSI"
    - "MACD"
  min_volume: 1000
  min_option_volume: 100
```

## Environment Variables

Required environment variables:
- `TD_API_KEY`: TD Ameritrade API key
- `TD_ACCOUNT_ID`: TD Ameritrade account ID
- `OPENAI_API_KEY`: OpenAI API key

## Logging Configuration

Customize logging in `logging_config.yaml`:
```yaml
version: 1
formatters:
  standard:
    format: '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    formatter: standard
    level: INFO
  file:
    class: logging.FileHandler
    filename: logs/trading.log
    formatter: standard
    level: DEBUG
```
```

```markdown:docs/api.md
# API Documentation

## Core Components

### Broker Interface

The `BaseBroker` class defines the standard interface for broker interactions:

```python
class BaseBroker(ABC):
    @abstractmethod
    async def connect(self):
        """Establish connection to broker API"""
        pass
    
    @abstractmethod
    async def get_option_chain(self, symbol: str) -> Dict:
        """Fetch option chain for given symbol"""
        pass
    
    # ... other methods
```

### Market Analysis

The `GPTAnalyzer` class handles market analysis:

```python
class GPTAnalyzer:
    async def analyze_market_conditions(self, market_data: Dict) -> Dict:
        """
        Analyze market conditions using GPT
        
        Args:
            market_data (Dict): Current market data
            
        Returns:
            Dict: Analysis results including:
                - sentiment: str ('bullish', 'bearish', 'neutral')
                - confidence: float (0-1)
                - recommendations: List[Dict]
        """
        pass
```

### Trading Strategy

The `OptionsStrategy` class implements trading logic:

```python
class OptionsStrategy:
    def generate_trade_signals(self, analysis: Dict, market_data: Dict) -> List[Dict]:
        """
        Generate trading signals
        
        Args:
            analysis (Dict): GPT analysis results
            market_data (Dict): Current market data
            
        Returns:
            List[Dict]: List of trade signals
        """
        pass
```

## Data Structures

### Market Data
```python
@dataclass
class OptionChain:
    calls: pd.DataFrame
    puts: pd.DataFrame
    underlying_price: float
    timestamp: datetime
```

### Trade Signal
```python
{
    'strategy_type': str,
    'direction': str,
    'symbol': str,
    'position_size': float,
    'entry_price': float,
    'stop_loss': float,
    'take_profit': float,
    'expiration': int,
    'strike_selection': Dict,
    'timestamp': str
}
```

## Error Handling

All components use structured error handling with logging:

```python
try:
    # Operation
except SpecificException as e:
    logger.error(f"Specific error: {str(e)}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
    raise
```
```

```markdown:docs/trading_strategies.md
# Trading Strategies

## Overview

The bot implements several options trading strategies based on market conditions and GPT analysis.

## Strategy Selection

Strategies are selected based on three main factors:
1. Market sentiment (bullish/bearish)
2. Volatility outlook (high/low)
3. Time horizon (short/medium/long)

## Available Strategies

### 1. Long Call
- **When Used**: Bullish sentiment + Low volatility
- **Risk Level**: Moderate
- **Time Horizon**: Short to medium
- **Max Loss**: Limited to premium paid
```python
{
    'strategy_type': 'long_call',
    'strike': current_price * 1.01  # Slightly OTM
}
```

### 2. Long Put
- **When Used**: Bearish sentiment + Low volatility
- **Risk Level**: Moderate
- **Time Horizon**: Short to medium
- **Max Loss**: Limited to premium paid
```python
{
    'strategy_type': 'long_put',
    'strike': current_price * 0.99  # Slightly OTM
}
```

### 3. Credit Put Spread
- **When Used**: Bullish sentiment + High volatility
- **Risk Level**: Defined risk
- **Time Horizon**: Short
- **Max Loss**: Difference between strikes minus premium
```python
{
    'strategy_type': 'credit_put_spread',
    'short_strike': current_price * 0.95,
    'long_strike': current_price * 0.93
}
```

### 4. Credit Call Spread
- **When Used**: Bearish sentiment + High volatility
- **Risk Level**: Defined risk
- **Time Horizon**: Short
- **Max Loss**: Difference between strikes minus premium
```python
{
    'strategy_type': 'credit_call_spread',
    'short_strike': current_price * 1.05,
    'long_strike': current_price * 1.07
}
```

## Risk Management

Each strategy includes:
- Position sizing rules
- Stop-loss levels
- Take-profit targets
- Maximum loss limits
- Delta/gamma exposure limits
```

```markdown:docs/risk_management.md
# Risk Management

## Overview

The risk management system implements multiple layers of protection:

1. Position-level risk controls
2. Portfolio-level risk controls
3. Daily trading limits
4. Sector exposure limits
5. Correlation controls

## Position Risk Controls

### Position Sizing
```python
def _calculate_position_size(self, market_data: Dict) -> float:
    account_size = self.config.get('account_size', 100000)
    risk_per_trade = self.config.get('risk_per_trade', 0.01)
    max_position_size = self.config.get('max_position_size', 5000)
    
    position_size = account_size * risk_per_trade
    return min(position_size, max_position_size)
```

### Stop Loss
- Automatically calculated based on technical levels
- Typically 1-2% below entry for long positions
- Adjusted based on volatility

### Take Profit
- Risk/reward ratio minimum 1:2
- Adjusted based on volatility and time horizon
- Can be trailing for trending markets

## Portfolio Risk Controls

### Maximum Positions
- Limited to 3 concurrent positions by default
- Adjustable in configuration

### Sector Exposure
- Maximum 30% exposure per sector
- Calculated based on position size

### Correlation
- Maximum correlation between positions: 0.7
- Helps ensure portfolio diversification

## Daily Controls

### Loss Limits
```python
def _check_daily_limits(self, trade: Dict) -> bool:
    max_daily_loss = self.config.get('max_daily_loss', 1000)
    max_daily_trades = self.config.get('max_daily_trades', 10)
    
    if abs(self.daily_loss) >= max_daily_loss:
        return False
    
    if self.daily_trades >= max_daily_trades:
        return False
    
    return True
```

### Trading Hours
- Only trades during market hours (9:30 AM - 4:00 PM ET)
- Adjustable in configuration

## Monitoring and Alerts

- Real-time position monitoring
- Automated alerts for:
  - Stop loss hits
  - Take profit hits
  - Risk limit breaches
  - Error conditions
```
