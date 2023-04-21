import json
import argparse
import bybit
import pybit
import config
from pybit.unified_trading import HTTP

parser = argparse.ArgumentParser()
parser.add_argument("--side", help="Trade side (Buy or Sell)", required=True)
args = parser.parse_args()
side = args.side

session = HTTP(
    testnet=False,
    api_key=config.your_api_key,
    api_secret=config.your_api_secret,
)

if side.lower() == "buy":
    print(session.place_order(
        category="linear",
        symbol="DOGEUSDT",
        side="Buy",
        orderType="Market",
        qty="500",
        reduce_only=True
    ))
    print(session.place_order(
        category="linear",
        symbol="DOGEUSDT",
        side="Buy",
        orderType="Market",
        qty="500",
        reduce_only=False
    ))

if side.lower() == "sell":
    print(session.place_order(
        category="linear",
        symbol="DOGEUSDT",
        side="Sell",
        orderType="Market",
        qty="500",
        reduce_only=True
    ))
    print(session.place_order(
        category="linear",
        symbol="DOGEUSDT",
        side="Sell",
        orderType="Market",
        qty="500",
        reduce_only=False
    ))
