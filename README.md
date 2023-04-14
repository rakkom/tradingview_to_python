# Overview
This bot receives alerts from TradingView as webhook and run python code to place orders on raspberry pi. The exchange this bot uses is Bybit and the pair is BTCUSDC. USDC pairs are free from trading fees. I will skip the set up details for raspberry pi. BICwA and darvasbox are names of strategies on TradingView.

1. TradingView --webhook--> smee --webhook--> webhook_listner.py on localhost (raspberry pi)

2. webhook_lisner.py --> BICwA.py OR darvasbox.py

3. cron --> checker_BICwA.py AND checker_darvasbox.py

## explanations for each code
1. listens to webhook alert from TradingView

2. places buy orders and creates json file to track the order records

3. places the counter orders and run every x hours to monitor order records and current price of btc

# External services and additional setup
This bot requires TradingView, smee and cron setup.

- TradingView: https://www.tradingview.com/

- smee: https://smee.io/

I used BICwA and darvasbox strategy as samples here. The code for these strategies are not provided in this repo. Therefore, you need to set up alerts on TradingView on your own. 

'''darvasbox.py and BICwA.py are 98% same. checker_BICwA.py and checker_darvasbox.py are also 98% same. But I needed json files for each separatedly, so I just copied and changed only the json file name.'''

You can set up raspberry pi system to run webhook_listner.py 24/7.
I recommend you to setup firewall and all necessary security setup as well due to smee.
