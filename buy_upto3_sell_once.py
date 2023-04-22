import os
import json
import argparse
import pybit
import config
from pybit.unified_trading import HTTP

def place_order(session, side, ticker, settings, reduce_only=False):
    try:
        response = session.place_order(
            category="linear",
            symbol=ticker,
            side=side,
            orderType="Market",
            qty=settings["qty"],
            reduce_only=reduce_only
        )
        print(response)
    except Exception as e:
        print(f"Error placing {side} order: {e}")

parser = argparse.ArgumentParser()
parser.add_argument("--side", help="Trade side (Buy or Sell)", choices=["buy", "sell"])
parser.add_argument("--ticker", help="Ticker symbol")
args = parser.parse_args()
side = args.side.lower()
ticker = args.ticker.upper()

if not ticker:
    print("Ticker symbol is required")
    exit(1)

ticker_filename = ticker.lower() + ".json"

try:
    with open(os.path.join("ticker_file", ticker_filename), "r") as f:
        settings = json.load(f)
except FileNotFoundError:
    settings = {"qty": "1"}

session = HTTP(
    testnet=False,
    api_key=config.api_key,
    api_secret=config.api_secret,
)

try:
    response_for_positions = session.get_positions(
        category="linear",
        symbol=ticker,
    )
    positions = response_for_positions['result']['list']
except Exception as e:
    print(f"Error fetching positions: {e}")
    exit(1)

has_long_position = False

for position in positions:
    if position['symbol'] == ticker:
        if position['side'].lower() == 'buy' and float(position['size']) > 0:
            has_long_position = True

if side == "buy":
        place_order(session, "Buy", ticker, settings)
elif side == "sell":
    if has_long_position:
        settings["qty"] = str(float(settings["qty"])*3)
        place_order(session, "Sell", ticker, settings, reduce_only=True)
