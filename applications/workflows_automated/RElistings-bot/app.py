from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from threading import Thread
from scripts.main import run_vinted_bot

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store bot state and logs in a simple dictionary
bot_state = {
    "running": False,
    "logs": []
}

def log_message(message):
    """
    Saves log messages to our global bot_state so we can display them in the UI.
    """
    bot_state["logs"].append(message)

@app.route("/")
def index():
    """
    Loads the main UI from the templates folder.
    """
    return render_template("index.html")

@app.route("/start-bot", methods=["POST"])
def start_bot():
    """
    Endpoint to start the Vinted bot.
    Expects JSON data with optional 'start_time' and 'interval' fields.
    """
    if bot_state["running"]:
        return jsonify({"status": "error", "message": "Bot is already running."}), 400

    data = request.json
    start_time = data.get("start_time", "06:00")
    interval = data.get("interval", 60)

    # Reset logs and update state
    bot_state["running"] = True
    bot_state["logs"] = []

    def bot_thread():
        try:
            run_vinted_bot(
                start_time=start_time,
                interval=interval,
                log_callback=log_message
            )
        finally:
            bot_state["running"] = False

    thread = Thread(target=bot_thread, daemon=True)
    thread.start()

    return jsonify({"status": "success", "message": "Bot started."})

@app.route("/stop-bot", methods=["POST"])
def stop_bot():
    """
    Endpoint to stop the Vinted bot (Not implemented here).
    """
    if not bot_state["running"]:
        return jsonify({"status": "error", "message": "Bot is not running."}), 400
    
    # You would need a mechanism in `run_vinted_bot` to safely stop the process.
    return jsonify({"status": "success", "message": "Stopping bot is not implemented."})

@app.route("/logs", methods=["GET"])
def get_logs():
    """
    Endpoint to retrieve the latest bot logs.
    """
    return jsonify({"status": "success", "logs": bot_state["logs"]})

if __name__ == "__main__":
    app.run(debug=True)