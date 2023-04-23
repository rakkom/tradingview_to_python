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

def place_order_with_reduce(session, ticker, side, qty):
    place_order(session, ticker, side, qty, reduce_only=True)
    place_order(session, ticker, side, qty)

parser = argparse.ArgumentParser()
parser.add_argument("--ticker", help="Ticker symbol")
parser.add_argument("--side", help="Trade side (Buy or Sell)")
parser.add_argument("--qty", help="Quantity")
args = parser.parse_args()
ticker = args.ticker.upper()
side = args.side.capitalize()
qty = args.qty

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

try:
    for position in positions:
        if position['symbol'] == ticker:
            if position['side'].lower() == 'buy' and float(position['size']) > 0:
                has_long_position = True
            elif position['side'].lower() == 'sell' and float(position['size']) > 0:
                has_short_position = True       
except Exception as e:
    print("Error caused by fetching position failure")
    exit(1)

if side == "Buy":
    if has_short_position:
        place_order_with_reduce(session, ticker, side, qty)
    else:
        place_order(session, ticker, side, qty)
elif side == "Sell":
    if has_long_position:
        place_order_with_reduce(session, ticker, side, qty)
    else:
        place_order(session, ticker, side, qty)
