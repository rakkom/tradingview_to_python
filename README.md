# Explanation
This bot receives alerts from TradingView as webhook and run python code to place orders on raspberry pi. The exchange this bot uses is Bybit and the pair is BTCUSDC. USDC pairs are free from trading fees. I will skip the set up details for raspberry pi.

TradingView --webhook--> smee --webhook--> webhook_listner.py on localhost (raspberry pi)

<it places buy orders and creates json file to track the order records>
webhook_lisner.py --> BICwA.py
                  --> darvasbox.py

<it places the counter orders and run every x hours to monitor order records and current price of btc>
cron --> checker_BICwA
     --> checker_darvasbox.py

# External services and additional setup
This bot requires TradingView, smee and cron setup.
TradingView: https://www.tradingview.com/
smee: https://smee.io/

I used BICwA and darvasbox strategy as samples here. The code for these strategies are not provided in this repo. Therefore, you need to set up alerts on TradingView on your own.

You can set up raspberry pi system to run webhook_listner.py 24/7.
I recommend you to setup firewall and all necessary security setup as well due to smee.
