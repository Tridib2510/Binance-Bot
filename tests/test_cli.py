import pytest
from unittest.mock import MagicMock, patch
from binance_client import BinanceFuturesClient
from cli import CLI


class TestCLI:
    def test_create_client_missing_env_vars(self, monkeypatch):
        monkeypatch.delenv("BINANCE_API_KEY", raising=False)
        monkeypatch.delenv("BINANCE_API_SECRET", raising=False)

        with pytest.raises(
            ValueError,
            match="BINANCE_API_KEY and BINANCE_API_SECRET environment variables are required",
        ):
            cli = CLI()

    @patch("binance_client.Client")
    def test_create_client_success(self, mock_client_class, monkeypatch):
        mock_client_instance = MagicMock()
        mock_client_class.return_value = mock_client_instance

        monkeypatch.setenv("BINANCE_API_KEY", "test_api_key")
        monkeypatch.setenv("BINANCE_API_SECRET", "test_api_secret")

        cli = CLI()
        assert cli.client is not None
