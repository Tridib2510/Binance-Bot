import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_binance_client():
    """Mock BinanceFuturesClient for testing."""
    with patch("binance_client.Client") as mock_client_class:
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        yield mock_client


@pytest.fixture
def sample_market_order_response():
    """Sample successful market order response."""
    return {
        "success": True,
        "data": {
            "orderId": "123456",
            "symbol": "BTCUSDT",
            "side": "BUY",
            "status": "FILLED",
            "type": "MARKET",
            "origQty": "0.001",
            "executedQty": "0.001",
            "avgPrice": "50000.00",
        },
        "error": None,
    }


@pytest.fixture
def sample_limit_order_response():
    """Sample successful limit order response."""
    return {
        "success": True,
        "data": {
            "orderId": "789012",
            "symbol": "ETHUSDT",
            "side": "SELL",
            "status": "NEW",
            "type": "LIMIT",
            "price": "3000.00",
            "origQty": "0.5",
            "executedQty": "0.0",
            "avgPrice": "0.00",
        },
        "error": None,
    }


@pytest.fixture
def sample_account_balance():
    """Sample account balance response."""
    return {
        "assets": [
            {"asset": "USDT", "walletBalance": "10000.0", "availableBalance": "9500.0"},
            {"asset": "BTC", "walletBalance": "0.001", "availableBalance": "0.001"},
        ]
    }


@pytest.fixture
def sample_position_info():
    """Sample position information response."""
    return [
        {
            "symbol": "BTCUSDT",
            "positionAmt": "0.001",
            "entryPrice": "49000.00",
            "markPrice": "50000.00",
            "unRealizedProfit": "1.0",
            "leverage": "10",
        }
    ]


@pytest.fixture
def error_response():
    """Sample error response."""
    return {
        "success": False,
        "data": None,
        "error": {"code": -2019, "message": "Insufficient balance"},
    }
