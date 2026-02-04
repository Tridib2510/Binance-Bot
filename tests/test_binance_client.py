import pytest
from unittest.mock import MagicMock, patch
from binance_client import OrderRequest, BinanceFuturesClient


class TestOrderRequest:
    def test_valid_market_order(self):
        order = OrderRequest(
            symbol="BTCUSDT", side="BUY", order_type="MARKET", quantity=0.001
        )
        is_valid, error = order.validate()
        assert is_valid is True
        assert error is None

    def test_valid_limit_order(self):
        order = OrderRequest(
            symbol="ETHUSDT",
            side="SELL",
            order_type="LIMIT",
            quantity=0.5,
            price=3000.0,
        )
        is_valid, error = order.validate()
        assert is_valid is True
        assert error is None

    def test_missing_symbol(self):
        order = OrderRequest(symbol="", side="BUY", order_type="MARKET", quantity=0.001)
        is_valid, error = order.validate()
        assert is_valid is False
        assert error == "Symbol is required"

    def test_invalid_side(self):
        order = OrderRequest(
            symbol="BTCUSDT", side="HOLD", order_type="MARKET", quantity=0.001
        )
        is_valid, error = order.validate()
        assert is_valid is False
        assert error == "Side must be BUY or SELL"

    def test_invalid_order_type(self):
        order = OrderRequest(
            symbol="BTCUSDT", side="BUY", order_type="STOP", quantity=0.001
        )
        is_valid, error = order.validate()
        assert is_valid is False
        assert error == "Order type must be MARKET or LIMIT"

    def test_negative_quantity(self):
        order = OrderRequest(
            symbol="BTCUSDT", side="BUY", order_type="MARKET", quantity=-0.001
        )
        is_valid, error = order.validate()
        assert is_valid is False
        assert error == "Quantity must be greater than 0"

    def test_zero_quantity(self):
        order = OrderRequest(
            symbol="BTCUSDT", side="BUY", order_type="MARKET", quantity=0.0
        )
        is_valid, error = order.validate()
        assert is_valid is False
        assert error == "Quantity must be greater than 0"

    def test_limit_order_without_price(self):
        order = OrderRequest(
            symbol="BTCUSDT", side="BUY", order_type="LIMIT", quantity=0.001, price=None
        )
        is_valid, error = order.validate()
        assert is_valid is False
        assert error == "Price is required for LIMIT orders and must be greater than 0"

    def test_limit_order_with_negative_price(self):
        order = OrderRequest(
            symbol="BTCUSDT",
            side="BUY",
            order_type="LIMIT",
            quantity=0.001,
            price=-50000.0,
        )
        is_valid, error = order.validate()
        assert is_valid is False
        assert error == "Price is required for LIMIT orders and must be greater than 0"

    def test_case_conversion(self):
        order = OrderRequest(
            symbol="btcusdt", side="buy", order_type="market", quantity=0.001
        )
        assert order.symbol == "btcusdt"
        assert order.side == "buy"
        assert order.order_type == "market"


class TestBinanceFuturesClient:
    @patch("binance_client.Client")
    def test_initialization(self, mock_client_class):
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance

        client = BinanceFuturesClient(
            api_key="test_key", api_secret="test_secret", testnet=True
        )
        assert client.testnet is True
        assert client.client is not None
        mock_client_class.assert_called_once_with(
            "test_key", "test_secret", testnet=True
        )

    @patch("binance_client.Client")
    def test_testnet_url(self, mock_client_class):
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance

        client = BinanceFuturesClient(
            api_key="test_key", api_secret="test_secret", testnet=True
        )
        assert client.testnet is True

    @patch("binance_client.Client")
    def test_mainnet_url(self, mock_client_class):
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance

        client = BinanceFuturesClient(
            api_key="test_key", api_secret="test_secret", testnet=False
        )
        assert client.testnet is False
        mock_client_class.assert_called_once_with(
            "test_key", "test_secret", testnet=False
        )
