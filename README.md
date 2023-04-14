# Overview
This bot receives alerts from **TradingView** as webhook and run python code to place orders on raspberry pi. The exchange this bot uses is **Bybit** and the pair is BTCUSDC. **USDC pairs are free from trading fees.** I skip the set up details for raspberry pi. BICwA and darvasbox are names of strategies on TradingView.

1. TradingView --webhook--> smee --webhook--> webhook_listner.py on localhost (raspberry pi)

2. webhook_lisner.py --> BICwA.py **OR** darvasbox.py

3. cron --> checker_BICwA.py **AND** checker_darvasbox.py

## explanations for each code
1. listens to webhook alert from TradingView

2. places buy orders and creates json file to track the order records

3. places the counter orders and run every x hours to monitor order records and current price of btc

# External services and additional setup
This bot requires TradingView, smee and cron setup, and of course Bybit.

- TradingView: https://www.tradingview.com/

- smee: https://smee.io/

- Bybit: https://www.bybit.com/

I used BICwA and darvasbox strategy as samples here. The code for these strategies are not provided in this repo. Therefore, you need to set up alerts on TradingView on your own. 

## TradvingView Alert format
Alerts from TradingView should look like this:

**{"strategy":"BICwA"}**

**{"strategy":"darvasbox"}**

# Usage

python webhook_listner.py
python checker_BICwA.py
python checker_darvasbox.py

# Full automation
You can set up **raspberry pi system to run webhook_listner.py 24/7** and set up **cron to run checker_xxx.py every x hours**.
I recommend you to setup firewall and all necessary security setup as well due to smee.
