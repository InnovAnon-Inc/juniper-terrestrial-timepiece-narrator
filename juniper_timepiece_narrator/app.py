#!/usr/bin/env python3
"""
juniper_terrestrial_timepiece_narrator.app
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Flask Server for the Terrestrial Timepiece Narrator.
"""

import os
import threading
from flask import Flask, render_template, jsonify, send_from_directory
from .narrator import TerrestrialTimepieceNarrator, CACHE_DIR

HTTP_PORT = int(os.environ.get("HTTP_PORT", 5019))
TIMEPIECE_URL = os.environ.get("TIMEPIECE_URL", "http://127.0.0.1:5008/api/timepiece_state")

app = Flask(__name__, template_folder="templates")
narrator = TerrestrialTimepieceNarrator(timepiece_url=TIMEPIECE_URL)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(CACHE_DIR, filename)


@app.route("/api/state")
def get_state():
    with narrator.lock:
        return jsonify(narrator.app_state)


def main():
    # Start Narrator polling thread
    threading.Thread(target=narrator.start_polling_loop, daemon=True).start()

    print(f"[TIMEPIECE NARRATOR SERVER] Running at http://0.0.0.0:{HTTP_PORT}")
    app.run(host="0.0.0.0", port=HTTP_PORT, debug=False)


if __name__ == "__main__":
    main()
