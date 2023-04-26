#!/usr/bin/env python3
# this part is necessary for cron

import json
import time
from datetime import datetime
import requests
import config
import os
from pybit import spot
from pprint import pprint

# Print current time for CRON
now = datetime.now()

current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"CRON job executed at: {current_timestamp}")
end_timestamp = datetime.fromtimestamp(datetime.now().timestamp())

# Load order records from JSON file. Pay attention to the name of the json file
with open('/home/user/order_records_bot.json', 'r') as f:
    order_records = json.load(f)

print('')
print('All order records')
print('')
print(order_records)
print('------------')
# Get current BTCUSDC spot price from Bybit API
session_unauth = spot.HTTP(
    endpoint="https://api.bybit.com"
)
current_price = session_unauth.last_traded_price(symbol="BTCUSDC")['result']['price']

# connect to bybit
session_auth = spot.HTTP(
    endpoint = "https://api.bybit.com",
    api_key=config.api_key,
    api_secret=config.api_secret
)

print('')
print('Order record, one by one')
# Check order records for sell opportunities
for record in order_records:
    print('')
    pprint(record)
    if record['sold checker'] == False:

        transact_time = int(record['result']['transactTime'])
        start_timestamp = datetime.fromtimestamp(transact_time / 1000)

        timedelta = end_timestamp - start_timestamp
        elapsed_days = timedelta.days
        qty = float(record['bought btc amount in this order'])

        print('----test----')
        print(f'elapsed_days:{elapsed_days}')
        print(f'end_timestamp:{end_timestamp}')
        print(f'start_timestamp:{start_timestamp}')
        print(record['current price'])
        print('----test----')
	
	# you can change the conditions here
        if elapsed_days >= 1 or (float(current_price) / float(record['current price']) - 1) >= 0.2:
            print('1 day has passed since the order or the price has been up by 20%, so I will place a sell order')
            # Place a market sell order on Bybit
            current_order = session_auth.place_active_order(
                symbol="BTCUSDC",
                side="Sell",
                type="MARKET",
                qty=qty,
                timeInForce="GTC"
            )

            # Update the order record
            record['sold checker'] = True
            print(record)
# Save the updated order records to JSON file
with open('order_records.json', 'w') as f:
    json.dump(order_records, f)
