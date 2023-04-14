from flask import Flask, request
import json
import subprocess

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        data = request.json
        strategy = data.get("strategy")
        side = data.get("side")

        if strategy == "BICwA":
            subprocess.run(["python", "BICwA.py"])

        elif strategy == "darvasbox":
            subprocess.run(["python", "darvasbox.py"])

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
