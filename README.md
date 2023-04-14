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
You have to run webhook_listner.py on your localhost.

```bash
python webhook_listner.py
```

You have to run checker_xxx.py every x hour manually.
```bash
python checker_BICwA.py
python checker_darvasbox.py
```

# Full automation
You can set up **raspberry pi system to run webhook_listner.py 24/7** and set up **cron to run checker_xxx.py every x hours**.
I recommend you to setup firewall and all necessary security setup as well due to smee.

## systemd setup for webhook_listner.py and smee
You need to run both smee and webhook_lisnter.py all the time. Therefore, it is better to set up system to run these 24/7.

```bash
sudo nano /etc/systemd/system/smee.service
```
```bash
[Unit] Description=Smee Webhook Tunnel Service After=network.target
[Service] ExecStart=/usr/bin/smee --url https://smee.io/UQCAjgN9ibszu9k --target http://localhost:5000/webhook WorkingDirectory=/home/pi/ StandardOutput=inherit StandardError=inherit Restart=always User=pi
[Install] WantedBy=multi-user.target
```

## cron setup
Edit cron. this command will open a file.
```bash
crontab -e
```
Set up time for cron. You can just copy paste it in the file. But make sure you replace * for what you want.
```bash
* * * * * /home/user/checker_BICwA.py >> /home/user/cronjob_BICwA.log 2>&1
* * * * * /home/user/checker_darvasbox.py >> /home/user/cronjob_darvasbox.log 2>&1
```

Give permissions to the python code to be run by cron.
```bash
chmod +x /home/user/checker_BICwA.py
chmod +x /home/user/checker_darvasbox.py
```

Check the status of cron and start cron. You need to manually start cron.
```bash
sudo systemctl status cron
sudo systemctl start cron
```
