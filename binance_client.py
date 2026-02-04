import os
import logging
from dataclasses import dataclass
from typing import Optional
import time
from functools import wraps

from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException

from logger import setup_logger

logger = setup_logger(__name__)


def retry_on_error(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except BinanceAPIException as e:
                    last_exception = e
                    error_msg = str(e.message) if hasattr(e, "message") else str(e)
                    if (
                        "502" in error_msg
                        or "503" in error_msg
                        or "504" in error_msg
                        or "Bad Gateway" in error_msg
                    ):
                        if attempt < max_retries - 1:
                            wait_time = delay * (attempt + 1)
                            logger.warning(
                                f"API error (attempt {attempt + 1}/{max_retries}): {error_msg}. "
                                f"Retrying in {wait_time}s..."
                            )
                            time.sleep(wait_time)
                            continue
                        else:
                            logger.error(
                                f"API error after {max_retries} attempts: {error_msg}"
                            )
                    raise
                except Exception as e:
                    if attempt < max_retries - 1:
                        wait_time = delay * (attempt + 1)
                        logger.warning(
                            f"Unexpected error (attempt {attempt + 1}/{max_retries}): {str(e)}. "
                            f"Retrying in {wait_time}s..."
                        )
                        time.sleep(wait_time)
                        continue
                    raise e
            if last_exception:
                logger.error(f"All retry attempts failed")
                raise last_exception
            raise Exception("Unknown error occurred")

        return wrapper

    return decorator


@dataclass
class OrderRequest:
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float] = None

    def validate(self) -> tuple[bool, Optional[str]]:
        if not self.symbol:
            return False, "Symbol is required"

        if self.side not in ["BUY", "SELL"]:
            return False, "Side must be BUY or SELL"

        if self.order_type not in ["MARKET", "LIMIT"]:
            return False, "Order type must be MARKET or LIMIT"

        if self.quantity <= 0:
            return False, "Quantity must be greater than 0"

        if self.order_type == "LIMIT" and (self.price is None or self.price <= 0):
            return (
                False,
                "Price is required for LIMIT orders and must be greater than 0",
            )

        logger.debug(
            f"Order validation: symbol={self.symbol}, side={self.side}, "
            f"type={self.order_type}, quantity={self.quantity}, price={self.price}"
        )
        return True, None


class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.testnet = testnet
        base_url = "testnet" if testnet else "fapi"
        logger.info(f"Initializing BinanceFuturesClient (network: {base_url})")
        self.client = Client(api_key, api_secret, testnet=testnet)
        logger.debug("Binance client initialized successfully")

        if testnet:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com"

    @retry_on_error(max_retries=3, delay=2)
    def place_order(self, order: OrderRequest) -> dict:
        logger.info(
            f"Placing order: {order.side} {order.quantity} {order.symbol} ({order.order_type})"
        )

        is_valid, error_msg = order.validate()
        if not is_valid:
            logger.error(f"Order validation failed: {error_msg}")
            raise ValueError(error_msg)

        params = {
            "symbol": order.symbol,
            "side": order.side,
            "type": order.order_type,
            "quantity": order.quantity,
            "timeInForce": "GTC" if order.order_type == "LIMIT" else None,
        }

        if order.order_type == "LIMIT":
            params["price"] = order.price

        if params["timeInForce"] is None:
            params.pop("timeInForce")

        logger.debug(f"Order parameters: {params}")

        try:
            response = self.client.futures_create_order(**params)
            logger.info(
                f"Order placed successfully. Order ID: {response.get('orderId')}"
            )
            return {"success": True, "data": response, "error": None}
        except BinanceAPIException as e:
            error_msg = str(e.message) if hasattr(e, "message") else str(e)
            logger.error(f"Binance API error: {error_msg} (code: {e.code})")
            return {
                "success": False,
                "data": None,
                "error": {"code": e.code, "message": error_msg},
            }
        except Exception as e:
            logger.error(f"Unexpected error placing order: {str(e)}")
            return {
                "success": False,
                "data": None,
                "error": {"code": -1, "message": str(e)},
            }
