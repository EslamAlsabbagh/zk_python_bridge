from flask import Flask, request
import bridge
from datetime import datetime

app = Flask(__name__)
SECRET = "Zksecret@2025"

@app.route('/')
def run_bridge():
    key = request.args.get("key")
    if key != SECRET:
        return "Unauthorized", 403
    try:
        bridge.main()
        return "Bridge executed"
    except Exception as e:
        return f"Error: {e}", 500



