import os
import json
import argparse
import pybit
import config
from pybit.unified_trading import HTTP

def place_order(session, ticker, side, qty, reduce_only=False):
    try:
        response = session.place_order(
            category="linear",
            symbol=ticker,
            side=side,
            orderType="Market",
            qty=qty,
            reduce_only=reduce_only
        )
        print(response)
    except Exception as e:
        print(f"Error placing {side} order: {e}")

parser = argparse.ArgumentParser()
parser.add_argument("--side", help="Buy or Sell")
parser.add_argument("--ticker", help="Ticker symbol")
parser.add_argument("--qty", help="Quantity")
args = parser.parse_args()
side = args.side.capitalize()
ticker = args.ticker.upper()
qty = args.qty

session = HTTP(
    testnet=False,
    api_key=config.api_key,
    api_secret=config.api_secret,
)

if side == "Buy":
        place_order(session, ticker, side, qty)
elif side == "Sell":
        place_order(session, ticker, side, qty, reduce_only=True)
