# Overview
This bot is designed to receive alerts from **TradingView** via webhook and execute Python code to place orders on a **Raspberry Pi**. It utilizes the **Bybit exchange** and operates with the **BTCUSDC** (SPOT) trading pair. Notably, USDC pairs are exempt from trading fees. The setup details for the Raspberry Pi will not be covered in this explanation. BICwA and darvasbox are the names of strategies employed within the TradingView platform.

1. TradingView --webhook--> smee --webhook--> webhook_listner.py on localhost (raspberry pi)

2. webhook_listner.py --> BICwA.py **OR** darvasbox.py

3. cron --> checker_BICwA.py **AND** checker_darvasbox.py

## Descriptions for each code segment
1. Receives webhook alerts from TradingView.

2. Executes buy orders and generates JSON files to keep track of order records.

3. Initiates counter orders based on previously generated the JSON files, running every specified number of hours to monitor order records and the current price of BTC.

The code related to webhook buys BTC under specific conditions based on predefined strategies, while the code related to cron checks regularly whether the sell conditions have been met or not.

# External services
This bot necessitates the setup of TradingView, Smee, Cron, and, naturally, Bybit.

- TradingView: https://www.tradingview.com/

- smee: https://smee.io/

- Bybit: https://www.bybit.com/

In this example, I employed the BICwA and darvasbox strategies as samples. However, the code for these strategies is not included in this repository. Consequently, you will need to configure alerts on TradingView independently.

## TradvingView Alert format
The alerts from TradingView should appear as follows:

**{"strategy":"BICwA"}**

**{"strategy":"darvasbox"}**

# § Usage: manual version 

It is recommended to use a virtual environment for this bot.

```bash
python3 -m venv myenv
source myenv/bin/activate
```

You will likely need to download some libraries to run this code. Some examples include:

```bash
pip install Flask
pip install pybit
pip install requests
```

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

# § Usage: automatic version
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
You need to enable webhook_listner by running this command.
```bash
sudo systemctl daemon-reload
sudo systemctl enable webhook_listener.service
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

You need to enable webhook_listner by running this command.
```bash
sudo systemctl daemon-reload
sudo systemctl enable smee.service
```

## Cron setup
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

# Comments
If you employ TradingView alerts for both buy and sell orders, setting up Cron is not necessary. However, you will need to modify the alert to include "side" data and subsequently adjust webhook_listener.py to accommodate these changes.

## TradvingView Alert format
The alerts from TradingView should appear as follows:

**{"strategy":"strategy_for_buy&sell","side":"{{strategy.order.action}}"}**

## webhook_listner.py
To accomplish this, you will need to pass the "side" data from the webhook to the "strategy_for_buy&sell.py" file.

```python
def handle_webhook():
    data = request.json
    strategy = data.get("strategy")
    side = data.get("side")

    if strategy == "strategy_for_buy&sell":
        subprocess.run(["python", "strategy_for_buy&sell.py", "--side", side])
    elif strategy == "BICwA":
        subprocess.run(["python", "BICwA.py"])

    return "OK"
 ```

## strategy_for_buy&sell.py
To be able to use the "side" data as an argument, you should include the following code in "strategy_for_buy&sell.py".

```python
import argparse

# Define the argument
parser = argparse.ArgumentParser()
parser.add_argument("--side", help="Side parameter")

# Parse and get the value of the argument
args = parser.parse_args()

# Display the value of the argument
print("Side parameter:", args.side)
```
