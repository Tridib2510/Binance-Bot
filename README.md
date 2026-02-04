# Binance Futures Trading Bot

A CLI and web-based bot with AI assistant for placing orders on Binance Futures Testnet (USDT-M).

## Features

- Place MARKET and LIMIT orders on Binance Futures Testnet
- Support both BUY and SELL orders
- Input validation
- Clear order request and response output
- **AI Assistant**: Chat-based interface using Groq (Llama 3.3) with LangChain tools
- **Streamlit Web UI**: Beautiful web interface with sidebar for API keys

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get Binance Testnet API credentials:
   - Go to [Binance Testnet](https://testnet.binancefuture.com/en/futures/BTC_USDT)
   - Register/login
   - Generate API Key and Secret in API Management

3. Get Groq API key:
   - Go to [Groq Console](https://console.groq.com/)
   - Sign up/login
   - Get your API key

## Usage

### Streamlit Web UI (Recommended)
Launch the web interface:
```bash
streamlit run app.py
```

Features:
- Enter API keys in sidebar
- Chat with AI assistant
- Real-time order placement
- Account balance and position info
- Chat history persistence

### CLI AI Assistant
Start the chat-based assistant (requires .env file):
```bash
python assistant.py
```

### Direct CLI Commands

#### Market Order
```bash
python main.py BTCUSDT BUY MARKET 0.001
```

#### Limit Order
```bash
python main.py BTCUSDT SELL LIMIT 0.001 50000
```

## Example Conversations

- "Place a market buy order for 0.001 BTC"
- "Sell 0.5 ETH at 3000"
- "Check my account balance"
- "What's my position on BTCUSDT?"
- "Buy 100 DOGE with a limit order at 0.15"

## Arguments (CLI Mode)

| Argument    | Description                          |
|------------|--------------------------------------|
| SYMBOL     | Trading pair (e.g., BTCUSDT)         |
| SIDE       | Order side: BUY or SELL              |
| ORDER_TYPE | Order type: MARKET or LIMIT          |
| QUANTITY   | Order quantity                        |
| PRICE      | Price (required for LIMIT orders)    |

## AI Assistant Tools

| Tool               | Description                                      |
|--------------------|--------------------------------------------------|
| place_market_order | Place MARKET orders (BUY or SELL)                |
| place_limit_order  | Place LIMIT orders with specified price          |
| get_account_balance| Check account balance                            |
| get_position_info  | Get position information for a trading pair     |

## Project Structure

```
binance-bot/
├── app.py            # Streamlit web UI
├── main.py           # CLI entry point
├── assistant.py      # CLI AI assistant
├── cli.py            # CLI command layer
├── binance_client.py # Binance API client layer
├── tools/            # LangChain tools
│   ├── __init__.py
│   ├── binance_tools.py   # Tools for CLI assistant
│   └── streamlit_tools.py # Tools for Streamlit UI
├── .env              # API credentials (not tracked)
├── .env.example      # Environment variables template
├── .gitignore
└── requirements.txt  # Python dependencies
```

## Testing

Run all tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=.
```

Run specific test file:
```bash
pytest tests/test_binance_client.py
```

Run tests with verbose output:
```bash
pytest -v
```

## Notes

- The bot uses Binance Futures Testnet (no real money involved)
- Make sure to use testnet API keys, not mainnet keys
- Streamlit UI does not require .env file - enter keys directly in sidebar
- Tests use mocking to avoid actual API calls to Binance
- **Proper logging** is implemented throughout the application

## Logging

The application includes comprehensive logging for debugging and monitoring:

- **INFO level** (default): Shows general operation flow
- **DEBUG level**: Shows detailed execution details
- **WARNING level**: Shows retry attempts and recoverable issues
- **ERROR level**: Shows failures and exceptions

See [LOGGING.md](LOGGING.md) for detailed logging configuration and examples.

### Example Log Output:
```
2024-02-04 13:45:30 - binance_client - INFO - Placing order: BUY 0.001 BTCUSDT (MARKET)
2024-02-04 13:45:31 - binance_client - INFO - Order placed successfully. Order ID: 123456
```

## Troubleshooting

If you encounter "502 Bad Gateway" errors, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for solutions.

**Quick Fix**: The code now includes automatic retry logic for 502 errors. If Binance Testnet is temporarily down, it will retry up to 3 times with delays.

**Pydantic Warning**: If you see "Pydantic V1 functionality isn't compatible with Python 3.14", consider using Python 3.11 or 3.12 instead.
