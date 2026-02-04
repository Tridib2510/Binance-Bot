# Troubleshooting Binance API Errors

## 502 Bad Gateway Error

If you're seeing "502 Bad Gateway" errors, this means the Binance Testnet API server is temporarily unavailable or experiencing issues.

### Common Causes:
1. **Binance Testnet is down** - The testnet API is often less stable than mainnet
2. **Network issues** - Temporary connectivity problems
3. **API rate limiting** - Too many requests in short time

### Solutions:

#### 1. Check Binance Testnet Status
- Visit https://testnet.binancefuture.com to see if the site is accessible
- Check Binance status page: https://status.binance.com/

#### 2. Retry Logic (Already Implemented)
The code now includes automatic retry logic for 502/503/504 errors:
- Retries up to 3 times
- Exponential backoff (2s, 4s, 6s delays)
- Handles network errors gracefully

#### 3. Use Different API Endpoints
If testnet continues to fail, you can try:
- **Testnet**: `https://testnet.binancefuture.com` (default)
- **Alternative**: Some users have better luck with different testnet instances

#### 4. Reduce Request Frequency
If making multiple requests:
- Add delays between requests
- Use batch operations when available
- Check account balance less frequently

#### 5. Verify API Credentials
Ensure your API keys are valid:
- Go to https://testnet.binancefuture.com/en/futures/BTC_USDT
- Login to your testnet account
- Navigate to API Management
- Generate new keys if needed
- Make sure API permissions include "Futures" trading

#### 6. Check Python Version
The warning "Pydantic V1 functionality isn't compatible with Python 3.14" suggests compatibility issues:
- Use Python 3.11 or 3.12 if possible
- Or wait for Pydantic/LangChain updates for Python 3.14

### Testing with Mock Data

If you just want to test the UI/agent without real API calls:

1. **Use the test suite:**
```bash
pytest tests/ -v
```

2. **Modify code to return mock data** for development/testing

### Alternative: Use Binance Mainnet

If testnet continues to be problematic, you can switch to mainnet (with real money):

In `binance_client.py`, change:
```python
client = Client(api_key, api_secret, testnet=False)
```

⚠️ **WARNING**: Only do this with test money first!

### Contacting Binance Support

If the issue persists:
- Report the issue at https://www.binance.com/en/support
- Mention: 502 errors on testnet
- Include your API key (public part only) and timestamp

### Code Improvements Added

1. **Retry Decorator**: Automatically retries failed API calls
2. **Better Error Messages**: Distinguishes between network errors and API errors
3. **Exponential Backoff**: Prevents overwhelming the server with retries

### Monitoring

To monitor if the issue is resolved:
- Try accessing https://testnet.binancefuture.com directly in a browser
- Run simple API test: `curl https://testnet.binancefuture.com/fapi/v1/ping`
- Check if other users are reporting similar issues online
