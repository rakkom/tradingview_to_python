# Overview
This bot is designed to receive alerts from **TradingView** via webhooks and execute Python code to place orders on a **Raspberry Pi**. It utilizes the **Bybit exchange** and operates with the **BTCUSDC** trading pair. Notably, USDC pairs are exempt from trading fees. The setup details for the Raspberry Pi will not be covered in this explanation. BICwA and darvasbox are the names of strategies employed within the TradingView platform.

1. TradingView --webhook--> smee --webhook--> webhook_listner.py on localhost (raspberry pi)

2. webhook_lisner.py --> BICwA.py **OR** darvasbox.py

3. cron --> checker_BICwA.py **AND** checker_darvasbox.py

## Descriptions for Each Code Segment
1. Receives webhook alerts from TradingView.

2. Executes buy orders and generates a JSON file to keep track of order records.

3. Initiates counter orders, running every specified number of hours to monitor order records and the current price of BTC.

# External services and additional setup
This bot necessitates the setup of TradingView, Smee, Cron, and, naturally, Bybit.

- TradingView: https://www.tradingview.com/

- smee: https://smee.io/

- Bybit: https://www.bybit.com/

In this example, I employed the BICwA and darvasbox strategies as samples. However, the code for these strategies is not included in this repository. Consequently, you will need to configure alerts on TradingView independently.

## TradvingView Alert format
The alerts from TradingView should appear as follows:

**{"strategy":"BICwA"}**

**{"strategy":"darvasbox"}**

# Usage: Manual version 
You must execute webhook_listener.py on your localhost.

```bash
python webhook_listner.py
```

You need to run this command, as well, for the smee connection.

```bash
smee --url https://smee.io/YOURSMEEURL --target http://localhost:5000/webhook
```

Additionally, you need to manually run checker_xxx.py every x hours.

```bash
python checker_BICwA.py
python checker_darvasbox.py
```

# Usage: automatatic version
To achieve full automation, configure your Raspberry Pi system to run webhook_listener.py continuously, 24/7, and schedule Cron to execute checker_xxx.py every x hours. It is also recommended to establish a firewall and implement any necessary security measures due to smee's involvement.

## systemd setup for webhook_listner.py and smee
Since both smee and webhook_listener.py need to run constantly, it is advisable to set up the system for 24/7 operation. Here is how.

### for webhook_listner.py
```bash
sudo nano /etc/systemd/system/webhook_listener.service
```
The file will open, allowing you to copy and paste the content. Replace the words in all capital letters with your relevant information.

```bash
[Unit] Description=Webhook Listener Service After=network.target
[Service] ExecStart=/usr/bin/python /home/USER/webhook_listener.py 
WorkingDirectory=/home/USER/ 
StandardOutput=inherit 
StandardError=inherit 
Restart=always 
User=PI
[Install] WantedBy=multi-user.target
```

### for smee
```bash
sudo nano /etc/systemd/system/smee.service
```
Again, the file will open, allowing you to copy and paste the content. Replace the words in all capital letters with your relevant information.

```bash
[Unit] Description=Smee Webhook Tunnel Service After=network.target
[Service] ExecStart=/usr/bin/smee --url https://smee.io/YOURSMEEURL --target http://localhost:5000/webhook 
WorkingDirectory=/home/USER/ 
StandardOutput=inherit 
StandardError=inherit 
Restart=always 
User=PI
[Install] WantedBy=multi-user.target
```

## cron setup
Edit Cron: This command will open the corresponding file for modification.

```bash
crontab -e
```
Configure the time settings for Cron. You can simply copy and paste the content into the file, but ensure that you replace the asterisks (*) with the desired values.

```bash
* * * * * /home/user/checker_BICwA.py >> /home/user/cronjob_BICwA.log 2>&1
* * * * * /home/user/checker_darvasbox.py >> /home/user/cronjob_darvasbox.log 2>&1
```

Grant the necessary permissions for the Python code to be executed by Cron.
```bash
chmod +x /home/user/checker_BICwA.py
chmod +x /home/user/checker_darvasbox.py
```

Verify the status of Cron and initiate it. Remember, you must manually start Cron.
```bash
sudo systemctl status cron
sudo systemctl start cron
```
