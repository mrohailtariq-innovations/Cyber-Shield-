from scapy.all import IP, TCP, UDP

# Professional Suspicious Ports List
# 8080: Common proxy/alt-web, 4444: Metasploit, 22: SSH (Bruteforce target)
SUSPICIOUS_PORTS = [22, 23, 4444, 5555, 8080, 8888]

def analyze_threats(packet):
    threat_message = ""

    if packet.haslayer(IP):
        src_ip = packet[IP].src
        
        # TCP Port Check
        if packet.haslayer(TCP):
            dst_port = packet[TCP].dport
            if dst_port in SUSPICIOUS_PORTS:
                threat_message = f"[!!!] SECURITY ALERT: Potential Unauthorized Access on Port {dst_port} from {src_ip}"
        
        # UDP Port Check (Malware often uses UDP)
        elif packet.haslayer(UDP):
            dst_port = packet[UDP].dport
            if dst_port in SUSPICIOUS_PORTS:
                threat_message = f"[!!!] SECURITY ALERT: Suspicious UDP Traffic on Port {dst_port} from {src_ip}"

    return threat_message