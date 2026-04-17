import datetime
import os

LOG_FILE = "data/logs/network_log.txt"

def log_packet(data):
    """
    Packet data ko timestamp ke saath file mein save karta hai.
    """
    # Ensure karein ke folder mojood hai
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {data}\n"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)