import os
import sys
from dotenv import load_dotenv

from cli import CLI


def main():
    load_dotenv()

    if len(sys.argv) < 5:
        print("Usage: python main.py <SYMBOL> <SIDE> <ORDER_TYPE> <QUANTITY> [PRICE]")
        print("\nArguments:")
        print("  SYMBOL      Trading pair (e.g., BTCUSDT)")
        print("  SIDE        Order side: BUY or SELL")
        print("  ORDER_TYPE   Order type: MARKET or LIMIT")
        print("  QUANTITY     Order quantity")
        print("  PRICE        Price (required for LIMIT orders)\n")
        print("\nExample:")
        print("  python main.py BTCUSDT BUY MARKET 0.001")
        print("  python main.py BTCUSDT SELL LIMIT 0.001 50000\n")
        sys.exit(1)

    symbol = sys.argv[1]
    side = sys.argv[2]
    order_type = sys.argv[3]
    quantity = float(sys.argv[4])
    price = float(sys.argv[5]) if len(sys.argv) > 5 else None

    cli = CLI()
    cli.run(
        symbol=symbol, side=side, order_type=order_type, quantity=quantity, price=price
    )


if __name__ == "__main__":
    main()
