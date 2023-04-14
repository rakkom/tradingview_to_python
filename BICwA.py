from pybit import spot
import json
import os
import config
from pprint import pprint


# connect to bybit
session_auth = spot.HTTP(
    endpoint="https://api.bybit.com",
    api_key=config.api_key,
    api_secret=config.api_secret
)

# check if json exits or not, each strategy needs each json file, so if you want to implement two or more strategies, you need another file
order_records_file = "order_records_BICwA.json"
if os.path.exists(order_records_file):
    with open(order_records_file, "r") as f:
        order_records = json.load(f)
else:
    order_records = []

# fetch current balance
current_balance = session_auth.get_wallet_balance()

# find out what coins you have in total
previous_btc_amount = 0
for balance in current_balance['result']['balances']:
    total = balance['total']
    coin = balance['coin']
    print(f'{coin} balance before order: {total} {coin}')
    if coin == 'BTC':
        previous_btc_amount = total

    # place a market order for BTCUSDC
    if coin == "USDC":
        btc_total = None
        for coin in session_auth.get_wallet_balance()['result']['balances']:
            if coin['coin'] == 'BTC':
                btc_total = coin['total']
                break

        if btc_total is not None:
            print('-----')
            print("Since you already have BTC in your account, I will compute the amount of BTC that will be bought in this order.")
            print('-----')
        else:
            print("BTC balance not found.")
            print('-----')

        current_order = session_auth.place_active_order(
            symbol="BTCUSDC",
            side="Buy",
            type="MARKET",
            qty=round(float(total)/10,2),
            timeInForce="GTC"
        )

        # fetch current balance
        next_balance = session_auth.get_wallet_balance()

        # find out what coins you have in total
        current_btc_amount = 0
        for balance in next_balance['result']['balances']:
            total = balance['total']
            coin = balance['coin']
            if coin == 'BTC':
                current_btc_amount = total
            print(f'{coin} balance after order: {total} {coin}')

        # calc the btc amount in this specific order
        btc_amount_in_this_order = float(current_btc_amount) - float(previous_btc_amount)

        # prepare a new element to be added to the json file
        current_order_id = current_order['result']['orderId']
        current_result = current_order['result']
        current_price = session_auth.last_traded_price(symbol="BTCUSDC")['result']['price']
        sold_checker = False

        print('calculating...')
        print(f"BTC amount purchased in this order: {btc_amount_in_this_order} BTC")
        new_element = {'orderId':current_order_id, 'result':current_result, 'current price': current_price, 'sold checker': sold_checker, 'bought btc amount in this order': btc_amount_in_this_order}
        order_records.append(new_element)

        print('-----')
        print('Adding a new element to the json file')
        pprint(order_records[-1])
        print('')

# writing in json
with open(order_records_file, "w") as f:
    json.dump(order_records, f)
