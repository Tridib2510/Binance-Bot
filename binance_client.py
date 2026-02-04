import os
from dataclasses import dataclass
from typing import Optional
import time
from functools import wraps

from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException


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
                    if (
                        "502" in str(e.message)
                        or "503" in str(e.message)
                        or "504" in str(e.message)
                        or "Bad Gateway" in str(e.message)
                    ):
                        if attempt < max_retries - 1:
                            time.sleep(delay * (attempt + 1))
                            continue
                    raise
                except Exception as e:
                    if attempt < max_retries - 1:
                        time.sleep(delay * (attempt + 1))
                        continue
                    raise e
            if last_exception:
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

        return True, None


class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.testnet = testnet
        self.client = Client(api_key, api_secret, testnet=testnet)

        if testnet:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com"

    @retry_on_error(max_retries=3, delay=2)
    def place_order(self, order: OrderRequest) -> dict:
        is_valid, error_msg = order.validate()
        if not is_valid:
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

        try:
            response = self.client.futures_create_order(**params)
            return {"success": True, "data": response, "error": None}
        except BinanceAPIException as e:
            return {
                "success": False,
                "data": None,
                "error": {"code": e.code, "message": e.message},
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": {"code": -1, "message": str(e)},
            }
