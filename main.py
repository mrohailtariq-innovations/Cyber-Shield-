import sys
import os
# Hum modules ko import kar rahay hain
from backend.sniffer import start_sniffing
from reporting.report_generator import generate_text_report

def show_menu():
    """Project ka main menu display karta hai"""
    print("\n" + "="*45)
    print("   🛡️  CYBERSECURITY PACKET SNIFFER PRO  🛡️")
    print("="*45)
    print(" 1. [TCP]    - Monitor Web & Apps Traffic")
    print(" 2. [UDP]    - Monitor Streaming & DNS")
    print(" 3. [ICMP]   - Monitor Ping Requests")
    print(" 4. [HTTP]   - Monitor Insecure Web Traffic")
    print(" 5. [ALL]    - Monitor Everything (Full Scan)")
    print(" 6. [REPORT] - Generate Summary from Logs")
    print(" 0. [EXIT]   - Close Program")
    print("="*45)

if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("\n[?] Select an option (0-6): ")

        if choice == "0":
            print("[*] Exiting... Allah Hafiz!")
            break
            
        elif choice == "6":
            print("\n[*] Manual Report Generation Triggered...")
            generate_text_report()
            
        elif choice in ["1", "2", "3", "4", "5"]:
            try:
                # Sniffing start karein
                start_sniffing(choice)
            except KeyboardInterrupt:
                # Jab user Ctrl+C dabaye ga
                print("\n\n" + "!"*40)
                print("[!] STOPPED: Sniffing halted by user.")
                print("[*] SAVING: Generating your security report...")
                
                # Report generate karne ka function call
                generate_text_report()
                
                print("[✔] SUCCESS: Report is ready in data/reports/")
                print("!"*40)
                input("\nPress Enter to return to menu...")
        else:
            print("[!] Error: Invalid selection. Try again.")