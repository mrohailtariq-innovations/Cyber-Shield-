from scapy.all import sniff, IP, TCP, UDP, ICMP, conf # conf add kiya
from filters.filter_engine import get_filter_string
from utils.logger import log_packet
from detection.detector import analyze_threats

def packet_callback(packet):
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        # Determine Protocol
        proto = "TCP" if packet.haslayer(TCP) else "UDP" if packet.haslayer(UDP) else "ICMP" if packet.haslayer(ICMP) else "Other"
        
        # Detection logic call karein
        alert = analyze_threats(packet)
        
        if alert:
            # Alert ko RED dikhayein
            print(f"\033[1;31m{alert}\033[0m")
            log_packet(alert)
        else:
            # Normal traffic ko normal dikhayein
            print(f"[+] {proto}: {src_ip} -> {dst_ip}")
            log_packet(f"{proto}: {src_ip} -> {dst_ip}")

# Is file mein koi major change nahi chahiye, bas ensure karein 
# ke aapka packet_callback print aur log dono kar raha hai.
def start_sniffing(filter_choice="5"):
    bpf_filter = get_filter_string(filter_choice)
    # store=False zaroori hai taake RAM full na ho
    sniff(filter=bpf_filter, prn=packet_callback, store=False)