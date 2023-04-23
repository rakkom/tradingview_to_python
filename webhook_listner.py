from flask import Flask, request
import json
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        data = request.json
        strategy = data.get("strategy")

        if strategy == "BICwA":
            subprocess.run(["python", "BICwA.py"])

        elif strategy == "darvasbox":
            subprocess.run(["python", "darvasbox.py"])

        elif strategy == "buy_and_sell":
            side = data.get("side")
            ticker = data.get("ticker")
            qty = data.get("qty")
            subprocess.run(["python", "buy_and_sell.py", "--side", side, "--ticker", ticker, "--qty", qty])           
            
        else:
            # raise an exception if strategy is not recognized
            raise ValueError("Invalid strategy")

        return "OK"

    except Exception as e:
        # log the error message
        app.logger.error(f"Error: {str(e)}")

        # return an error response to the client
        return {"error": str(e)}, 400

if __name__ == '__main__':
    app.run(debug=True)
