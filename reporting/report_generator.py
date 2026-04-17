import os
from datetime import datetime

def generate_text_report():
    """
    Log file ko read karke ek summary report generate karta hai.
    """
    LOG_FILE = "data/logs/network_log.txt"
    REPORT_DIR = "data/reports"
    
    # Check karein ke logs mojood hain ya nahi
    if not os.path.exists(LOG_FILE):
        print(f"[!] Error: Log file '{LOG_FILE}' nahi mili.")
        return

    # Reports folder banayein agar nahi hai
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)

    # Log file read karein
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    total_entries = len(lines)
    alerts = [l for l in lines if "[!!!]" in l]
    total_alerts = len(alerts)
    
    report_name = "summary_report.txt"
    report_path = os.path.join(REPORT_DIR, report_name)
    
    report_content = f"""
=============================================
      NETWORK SNIFFER SECURITY REPORT
=============================================
Total Packets Logged: {total_entries}
Total Security Alerts: {total_alerts}
---------------------------------------------
"""
    with open(report_path, "w") as f:
        f.write(report_content)

    print(f"\n[✔] SUCCESS: Report saved at: {report_path}")