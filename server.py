from flask import Flask, request
import bridge
import logging
from datetime import datetime

app = Flask(__name__)
SECRET = "Zksecret@2025"

# Setup logging
logging.basicConfig(
    filename="zk_bridge.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.route('/')
def run_bridge():
    key = request.args.get("key")
    if key != SECRET:
        logging.warning(f"Unauthorized access attempt from {request.remote_addr}")
        return "Unauthorized", 403

    logging.info("Bridge triggered successfully")
    try:
        zk_bridge.main()
        logging.info("Bridge executed successfully")
        return "Bridge executed"
    except Exception as e:
        logging.error(f"Bridge execution failed: {e}")
        return f"Error: {e}", 500


