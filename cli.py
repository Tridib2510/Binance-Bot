import os
import logging
from typing import Optional

from binance_client import BinanceFuturesClient, OrderRequest
from logger import setup_logger

logger = setup_logger(__name__)


class CLI:
    def __init__(self):
        self.client = self._create_client()

    def _create_client(self) -> BinanceFuturesClient:
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            logger.error(
                "BINANCE_API_KEY and BINANCE_API_SECRET environment variables are required"
            )
            raise ValueError(
                "BINANCE_API_KEY and BINANCE_API_SECRET environment variables are required"
            )

        logger.info("CLI client initialized successfully")
        return BinanceFuturesClient(api_key, api_secret, testnet=True)

    def _print_order_summary(self, order: OrderRequest):
        print("\n=== Order Request Summary ===")
        print(f"Symbol:    {order.symbol}")
        print(f"Side:      {order.side}")
        print(f"Type:      {order.order_type}")
        print(f"Quantity:  {order.quantity}")
        if order.order_type == "LIMIT":
            print(f"Price:     {order.price}")
        print("============================\n")

    def _print_order_response(self, response: dict):
        if response["success"]:
            data = response["data"]
            print("=== Order Response ===")
            print(f"Order ID:      {data.get('orderId', 'N/A')}")
            print(f"Status:        {data.get('status', 'N/A')}")
            print(f"Symbol:        {data.get('symbol', 'N/A')}")
            print(f"Side:          {data.get('side', 'N/A')}")
            print(f"Type:          {data.get('type', 'N/A')}")
            print(f"Quantity:      {data.get('origQty', 'N/A')}")
            print(f"Executed Qty:  {data.get('executedQty', 'N/A')}")
            print(f"Avg Price:     {data.get('avgPrice', 'N/A')}")
            print("======================")
            print("\n✅ Order placed successfully!\n")
        else:
            error = response["error"]
            print("=== Order Failed ===")
            print(f"Error Code:    {error.get('code', 'N/A')}")
            print(f"Error Message: {error.get('message', 'N/A')}")
            print("====================")
            print("\n❌ Failed to place order!\n")

    def run(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
    ) -> None:
        logger.info(f"Running CLI command: {side} {quantity} {symbol} ({order_type})")

        try:
            order = OrderRequest(
                symbol=symbol.upper(),
                side=side.upper(),
                order_type=order_type.upper(),
                quantity=quantity,
                price=price,
            )

            self._print_order_summary(order)

            response = self.client.place_order(order)

            self._print_order_response(response)

        except ValueError as e:
            logger.error(f"Validation error: {e}")
            print(f"\n❌ Validation Error: {e}\n")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"\n❌ Unexpected Error: {e}\n")
