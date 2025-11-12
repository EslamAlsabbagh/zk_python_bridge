from zk import ZK
import requests
import json
from datetime import datetime

print("ZK Bridge Script Started")
def main():
        # ==== CONFIG ====
    DEVICE_IP = "196.151.241.119"
    PORT = 4370
    COMM_KEY = 0  # change if device has a comm password
    SUPABASE_FUNCTION_URL = "https://onkzdfbifygmobauuqhe.supabase.co/functions/v1/uploadAttendance"
    SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9ua3pkZmJpZnlnbW9iYXV1cWhlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE3NTMwNzcsImV4cCI6MjA3NzMyOTA3N30.61hmVL3vo4furDssA99FrCt8ZH8djScv8KAKPXsiysM"

    # =================

    zk = ZK(DEVICE_IP, port=PORT, timeout=10, password=COMM_KEY)
    conn = None
    print("Script started")

    try:
        print(f"Connecting to device {DEVICE_IP}...")
        conn = zk.connect()
        print("Connected")
        conn.disable_device()

        attendance = conn.get_attendance()
        print(f"Downloaded {len(attendance)} attendance records")

        logs = []
        for att in attendance:
            logs.append({
                "user_id": att.user_id,
                "timestamp": att.timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
                "status": att.status,
            })

        if logs:
            res = requests.post(
                SUPABASE_FUNCTION_URL,
                headers={
                    "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
                    "Content-Type": "application/json"
                },
                data=json.dumps({"logs": logs})
            )
            print("Supabase response:", res.status_code, res.text)
        else:
            print("No new attendance logs.")

        conn.enable_device()

    except Exception as e:
        print("Error:", e)

    finally:
        if conn:
            conn.disconnect()


