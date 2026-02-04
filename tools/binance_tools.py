import os
from typing import Optional

from binance_client import BinanceFuturesClient, OrderRequest
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()


def get_client() -> BinanceFuturesClient:
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError(
            "BINANCE_API_KEY and BINANCE_API_SECRET environment variables are required"
        )

    return BinanceFuturesClient(api_key, api_secret, testnet=True)


@tool
def place_market_order(symbol: str, side: str, quantity: float) -> str:
    """
    Place a MARKET order on Binance Futures Testnet.

    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        side: Order side - either 'BUY' or 'SELL'
        quantity: Order quantity

    Returns:
        Order response details including orderId, status, executedQty, avgPrice
    """
    try:
        client = get_client()
        order = OrderRequest(
            symbol=symbol.upper(),
            side=side.upper(),
            order_type="MARKET",
            quantity=quantity,
        )

        response = client.place_order(order)

        if response["success"]:
            data = response["data"]
            return (
                f"✅ MARKET order placed successfully!\n"
                f"Order ID: {data.get('orderId', 'N/A')}\n"
                f"Symbol: {data.get('symbol', 'N/A')}\n"
                f"Side: {data.get('side', 'N/A')}\n"
                f"Status: {data.get('status', 'N/A')}\n"
                f"Quantity: {data.get('origQty', 'N/A')}\n"
                f"Executed Qty: {data.get('executedQty', 'N/A')}\n"
                f"Avg Price: {data.get('avgPrice', 'N/A')}"
            )
        else:
            error = response["error"]
            return (
                f"❌ Order failed!\n"
                f"Error Code: {error.get('code', 'N/A')}\n"
                f"Error Message: {error.get('message', 'N/A')}"
            )
    except Exception as e:
        return f"❌ Error placing order: {str(e)}"


@tool
def place_limit_order(symbol: str, side: str, quantity: float, price: float) -> str:
    """
    Place a LIMIT order on Binance Futures Testnet.

    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)
        side: Order side - either 'BUY' or 'SELL'
        quantity: Order quantity
        price: Limit price for the order

    Returns:
        Order response details including orderId, status, executedQty, avgPrice
    """
    try:
        client = get_client()
        order = OrderRequest(
            symbol=symbol.upper(),
            side=side.upper(),
            order_type="LIMIT",
            quantity=quantity,
            price=price,
        )

        response = client.place_order(order)

        if response["success"]:
            data = response["data"]
            return (
                f"✅ LIMIT order placed successfully!\n"
                f"Order ID: {data.get('orderId', 'N/A')}\n"
                f"Symbol: {data.get('symbol', 'N/A')}\n"
                f"Side: {data.get('side', 'N/A')}\n"
                f"Status: {data.get('status', 'N/A')}\n"
                f"Price: {data.get('price', 'N/A')}\n"
                f"Quantity: {data.get('origQty', 'N/A')}\n"
                f"Executed Qty: {data.get('executedQty', 'N/A')}\n"
                f"Avg Price: {data.get('avgPrice', 'N/A')}"
            )
        else:
            error = response["error"]
            return (
                f"❌ Order failed!\n"
                f"Error Code: {error.get('code', 'N/A')}\n"
                f"Error Message: {error.get('message', 'N/A')}"
            )
    except Exception as e:
        return f"❌ Error placing order: {str(e)}"


@tool
def get_account_balance() -> str:
    """
    Get the account balance for Binance Futures Testnet.

    Returns:
        Account balance information including available balance and asset details
    """
    try:
        client = get_client()
        account_info = client.client.futures_account()

        balance_info = []
        for balance in account_info.get("assets", []):
            if float(balance["walletBalance"]) > 0:
                balance_info.append(
                    f"Asset: {balance['asset']}\n"
                    f"Wallet Balance: {balance['walletBalance']}\n"
                    f"Available Balance: {balance['availableBalance']}"
                )

        if balance_info:
            return "📊 Account Balance:\n\n" + "\n\n".join(balance_info)
        else:
            return "No balance found in account."

    except Exception as e:
        return f"❌ Error fetching account balance: {str(e)}"


@tool
def get_position_info(symbol: str) -> str:
    """
    Get position information for a specific trading pair.

    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)

    Returns:
        Position details including position size, entry price, unrealized profit/loss
    """
    try:
        client = get_client()
        positions = client.client.futures_position_information(symbol=symbol.upper())

        if positions:
            pos = positions[0]
            if float(pos["positionAmt"]) != 0:
                return (
                    f"📈 Position Information for {pos['symbol']}:\n"
                    f"Position Size: {pos['positionAmt']}\n"
                    f"Entry Price: {pos['entryPrice']}\n"
                    f"Mark Price: {pos['markPrice']}\n"
                    f"Unrealized PnL: {pos['unRealizedProfit']}\n"
                    f"Leverage: {pos['leverage']}"
                )
            else:
                return f"No open position for {symbol}"
        else:
            return f"No position information found for {symbol}"

    except Exception as e:
        return f"❌ Error fetching position info: {str(e)}"


tools = [place_market_order, place_limit_order, get_account_balance, get_position_info]
