def get_filter_string(choice):
    """
    User ki choice ke mutabiq BPF filter string return karta hai.
    """
    filters = {
        "1": "tcp",
        "2": "udp",
        "3": "icmp",
        "4": "port 80 or port 443", # Web traffic
        "5": "" # No filter (All traffic)
    }
    return filters.get(choice, "")