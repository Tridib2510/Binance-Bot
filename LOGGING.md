# Logging Configuration

This project uses Python's built-in logging module for comprehensive debugging and monitoring.

## Logging Levels

The logger supports the following standard logging levels:

- **DEBUG**: Detailed information for diagnosing problems
- **INFO**: General information about program execution
- **WARNING**: Something unexpected happened, but software is still working
- **ERROR**: Due to a more serious problem, software has not been able to perform some function
- **CRITICAL**: Serious error, indicating that the program itself may be unable to continue

## Default Configuration

By default, the logging level is set to **INFO**. This includes:
- Initialization messages
- API calls and responses
- Order placements
- Tool invocations
- General operation flow

## Changing Log Level

### For CLI/Assistant:

Edit `logger.py` and change the level in the `setup_logger` function call:

```python
logger = setup_logger(__name__, level="DEBUG")  # For detailed logs
logger = setup_logger(__name__, level="WARNING")  # For minimal logs
```

### For Streamlit:

The logger level can be configured via environment variable. Add to `.env`:

```bash
LOG_LEVEL=DEBUG
```

Then modify `logger.py` to read this:

```python
log_level = os.getenv("LOG_LEVEL", "INFO")
logger = setup_logger(__name__, level=log_level)
```

## Log Format

Logs are formatted as:
```
YYYY-MM-DD HH:MM:SS - <module_name> - <LEVEL> - <message>
```

Example:
```
2024-02-04 13:45:30 - binance_client - INFO - Placing order: BUY 0.001 BTCUSDT (MARKET)
2024-02-04 13:45:31 - binance_client - INFO - Order placed successfully. Order ID: 123456
```

## What Gets Logged

### binance_client.py

**INFO Level:**
- Client initialization (testnet/mainnet)
- Order placement start
- Successful order placement with Order ID
- Retry attempts for 502 errors

**DEBUG Level:**
- Order validation details
- Order parameters
- Order parameters sent to Binance

**WARNING Level:**
- API retry attempts (502/503/504 errors)
- Rate limiting or temporary failures

**ERROR Level:**
- API errors from Binance
- Failed order placements
- Unexpected exceptions
- All retry attempts exhausted

### cli.py

**INFO Level:**
- CLI command execution
- Client initialization

**ERROR Level:**
- Validation errors
- Unexpected errors during execution

### tools/binance_tools.py

**INFO Level:**
- Tool invocations (which tool called)
- Successful order placements
- Account balance retrieval (with asset count)
- Position information retrieval
- Tools loaded on module import

**DEBUG Level:**
- Order validation details
- Account info retrieved
- Position info retrieved

**WARNING Level:**
- No balance found in account
- No open position for symbol
- No position information found

**ERROR Level:**
- Tool execution errors
- API errors (with code and message)
- Failed order placements

### tools/streamlit_tools.py

Same as `binance_tools.py`, logs all tool-related events.

### assistant.py

**INFO Level:**
- Assistant startup
- Agent creation
- Model configuration
- User exit requests

**DEBUG Level:**
- User input messages

**ERROR Level:**
- Environment variable errors
- Error processing user input

### app.py

**INFO Level:**
- Application startup
- Agent creation
- Tool loading
- User input received
- Agent responses received

**DEBUG Level:**
- Agent invocation details
- Chat history details

**ERROR Level:**
- Error processing agent response
- Exception handling for user interactions

## Example Logs

### Successful Order Placement:
```
2024-02-04 13:45:30 - binance_client - INFO - Initializing BinanceFuturesClient (network: testnet)
2024-02-04 13:45:30 - binance_client - INFO - Placing order: BUY 0.001 BTCUSDT (MARKET)
2024-02-04 13:45:30 - binance_client - DEBUG - Order parameters: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.001}
2024-02-04 13:45:31 - binance_client - INFO - Order placed successfully. Order ID: 123456
2024-02-04 13:45:31 - binance_tools - INFO - Tool invoked: place_market_order(BTCUSDT, BUY, 0.001)
2024-02-04 13:45:31 - binance_tools - INFO - Market order placed successfully. Order ID: 123456
```

### Error with Retry:
```
2024-02-04 13:45:30 - binance_client - INFO - Placing order: BUY 0.001 BTCUSDT (MARKET)
2024-02-04 13:45:31 - binance_client - WARNING - API error (attempt 1/3): 502 Bad Gateway. Retrying in 2s...
2024-02-04 13:45:33 - binance_client - WARNING - API error (attempt 2/3): 502 Bad Gateway. Retrying in 4s...
2024-02-04 13:45:37 - binance_client - INFO - Order placed successfully. Order ID: 123456
```

### API Error:
```
2024-02-04 13:45:30 - binance_client - INFO - Placing order: BUY 0.001 BTCUSDT (MARKET)
2024-02-04 13:45:31 - binance_client - ERROR - Binance API error: Insufficient balance (code: -2019)
2024-02-04 13:45:31 - binance_tools - ERROR - Market order failed: Insufficient balance (code: -2019)
```

## Troubleshooting

### Too Many Logs?

If you see too many logs at INFO level, change to WARNING:

```python
# In each file that imports logger
logger = setup_logger(__name__, level="WARNING")
```

### Not Enough Detail?

If you need more detail to debug an issue:

```python
# In each file that imports logger
logger = setup_logger(__name__, level="DEBUG")
```

### Debugging 502 Errors

When Binance returns 502 Bad Gateway, you'll see:
```
WARNING - API error (attempt 1/3): 502 Bad Gateway. Retrying in 2s...
```

This helps you understand that:
1. The error occurred
2. It's being retried automatically
3. How many retries are remaining

### Capturing Logs to File

To save logs to a file, modify `logger.py`:

```python
def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (add this)
    file_handler = logging.FileHandler('binance_bot.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
```

## Best Practices

1. **Use appropriate levels:**
   - Use `logger.debug()` for detailed information
   - Use `logger.info()` for general flow
   - Use `logger.warning()` for recoverable issues
   - Use `logger.error()` for serious problems

2. **Include context:**
   - Log what (symbol, quantity, side)
   - Log why (operation being performed)
   - Log result (success/failure with details)

3. **Don't log sensitive data:**
   - Never log full API secrets
   - Only log partial or masked values when necessary

4. **Structured messages:**
   - Start with action verb: "Placing order", "Retrieving balance"
   - Include key details in message
   - Be consistent in naming
