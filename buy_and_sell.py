import json
import argparse
import os
import bybit
import pybit
import config
from pybit.unified_trading import HTTP

parser = argparse.ArgumentParser()
parser.add_argument("--side", help="Trade side (Buy or Sell)")
parser.add_argument("--ticker", help="Ticker symbol")
args = parser.parse_args()
side = args.side
ticker = args.ticker

if args.ticker:
    ticker_filename = args.ticker.lower() + ".json"
    with open(os.path.join("ticker_file", ticker_filename), "r") as f:
        settings = json.load(f)
else:
    settings = {"qty": "1"}

session = HTTP(
    testnet=False,
    api_key=config.api_key,
    api_secret=config.api_secret,
)

if side.lower() == "buy":
    print(session.place_order(
        category="linear",
        symbol=ticker,
        side="Buy",
        orderType="Market",
        qty=settings["qty"],
        reduce_only=True
    ))
    print(session.place_order(
        category="linear",
        symbol=ticker,
        side="Buy",
        orderType="Market",
        qty=settings["qty"],
        reduce_only=False
    ))

if side.lower() == "sell":
    print(session.place_order(
        category="linear",
        symbol=ticker,
        side="Sell",
        orderType="Market",
        qty=settings["qty"],
        reduce_only=True
    ))
    print(session.place_order(
        category="linear",
        symbol=ticker,
        side="Sell",
        orderType="Market",
        qty=settings["qty"],
        reduce_only=False
    ))
