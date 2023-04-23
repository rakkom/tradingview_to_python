import os
import json
import argparse
import pybit
import config
from pybit.unified_trading import HTTP

def place_order(session, side, ticker, qty, reduce_only=False):
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

def order_with_reduce_only(session, side, ticker, qty):
    place_order(session, side, ticker, qty, reduce_only=True)
    place_order(session, side, ticker, qty)

parser = argparse.ArgumentParser()
parser.add_argument("--side", help="Trade side (Buy or Sell)", choices=["buy", "sell"])
parser.add_argument("--ticker", help="Ticker symbol")
parser.add_argument("--qty", help="Quantity")
args = parser.parse_args()

side = args.side.capitalize()
ticker = args.ticker.upper()
qty = args.qty

if not ticker:
    print("Ticker symbol is required")
    exit(1)

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
has_short_position = False

for position in positions:
    if position['symbol'] == ticker:
        if position['side'].lower() == 'buy' and float(position['size']) > 0:
            has_long_position = True
        elif position['side'].lower() == 'sell' and float(position['size']) > 0:
            has_short_position = True

if side == "Buy":
    if has_short_position:
        order_with_reduce_only(session, side, ticker, qty)
    else:
        place_order(session, side, ticker, qty)
elif side == "Sell":
    if has_long_position:
        order_with_reduce_only(session, ticker, qty)
    else:
        place_order(session, side, ticker, qty)