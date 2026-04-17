import streamlit as st
import multiprocessing
import os
import time
import pandas as pd
from backend.sniffer import start_sniffing
from reporting.report_generator import generate_text_report

# ──────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ──────────────────────────────────────────────────────────────────────────────
if "sniffer_process" not in st.session_state:
    st.session_state.sniffer_process = None

LOG_FILE = "data/logs/network_log.txt"

# ──────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cyber Shield | M.Rohail 043",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
#  GLOBAL CSS — NEON CYBER DARK THEME
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600&display=swap');

html, body, [class*="css"], .stApp {
    background-color: #030810 !important;
    color: #a0c8b0 !important;
    font-family: 'Rajdhani', sans-serif !important;
}
.main .block-container {
    padding-top: 1rem !important;
    padding-bottom: 4rem !important;
    max-width: 1440px !important;
}

[data-testid="stSidebar"] {
    background: #040c14 !important;
    border-right: 1px solid #00ff9918 !important;
}
[data-testid="stSidebar"] > div { padding-top: 0 !important; }
[data-testid="stSidebar"] * { color: #a0c8b0 !important; }

.stSelectbox > div > div {
    background: #060f1a !important;
    border: 1px solid #00ff9930 !important;
    color: #00e5ff !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 12px !important;
    border-radius: 4px !important;
}
.stSelectbox svg { fill: #00ff9966 !important; }

div[data-testid="column"]:nth-child(1) .stButton > button {
    background: #001a0d !important;
    color: #00ff99 !important;
    border: 1px solid #00ff9960 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 2px !important;
    border-radius: 4px !important;
    width: 100% !important;
    padding: 10px 6px !important;
}
div[data-testid="column"]:nth-child(1) .stButton > button:hover {
    background: #003322 !important;
    border-color: #00ff99 !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button {
    background: #1a0007 !important;
    color: #ff3366 !important;
    border: 1px solid #ff336660 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 2px !important;
    border-radius: 4px !important;
    width: 100% !important;
    padding: 10px 6px !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button:hover {
    background: #330010 !important;
    border-color: #ff3366 !important;
}

div[data-testid="stTable"] table {
    background: #040b12 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 11px !important;
    width: 100% !important;
    border-collapse: collapse !important;
}
div[data-testid="stTable"] thead tr {
    background: #050e18 !important;
    border-bottom: 1px solid #00ff9925 !important;
}
div[data-testid="stTable"] th {
    color: #00e5ff !important;
    letter-spacing: 2px !important;
    font-size: 10px !important;
    padding: 9px 12px !important;
    text-transform: uppercase !important;
}
div[data-testid="stTable"] td {
    color: #7fffd4 !important;
    border-bottom: 1px solid #00ff9908 !important;
    padding: 8px 12px !important;
}
div[data-testid="stTable"] tr:hover td { background: #061018 !important; }

div[data-testid="stAlert"] {
    background: #040c14 !important;
    border-radius: 4px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 11px !important;
    border: none !important;
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #040c14; }
::-webkit-scrollbar-thumb { background: #00ff9930; border-radius: 2px; }

.stMarkdown p { margin-bottom: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
#  HEADER BANNER
# ──────────────────────────────────────────────────────────────────────────────
is_running = (
    st.session_state.sniffer_process is not None
    and st.session_state.sniffer_process.is_alive()
)
sys_color = "#00ff99" if is_running else "#1a5040"
sys_label = "ACTIVE" if is_running else "ONLINE"

st.markdown(f"""
<div style="background:#020608;border:1px solid #00ff9920;border-radius:8px;
            padding:14px 24px;margin-bottom:12px;display:flex;align-items:center;gap:16px;">
    <div>
        <div style="font-family:'Orbitron',sans-serif;font-size:26px;font-weight:900;
                    color:#00ff99;letter-spacing:5px;">
            CYBER<span style="color:#00e5ff;">SHIELD</span>
        </div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:9px;color:#1a4a35;
                    letter-spacing:3px;margin-top:4px;">
            DEVELOPED BY M.Rohail 043 PROJECT &nbsp;&#9670;&nbsp; NETWORK INTELLIGENCE PLATFORM v2.4
        </div>
    </div>
    <div style="margin-left:auto;text-align:right;">
        <div style="font-family:'Share Tech Mono',monospace;font-size:8px;
                    color:#0a3025;letter-spacing:3px;">SYS STATUS</div>
        <div style="font-family:'Orbitron',sans-serif;font-size:14px;font-weight:700;
                    color:{sys_color};letter-spacing:3px;">&#9679; {sys_label}</div>
    </div>
</div>
<div style="height:2px;background:#00ff9914;border-radius:1px;margin-bottom:14px;"></div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:

    st.markdown("""
    <div style="background:#020608;border-bottom:1px solid #00ff9918;
                padding:14px 14px 12px;margin:-1rem -1rem 14px -1rem;">
        <div style="font-family:'Orbitron',sans-serif;font-size:14px;font-weight:700;
                    color:#00ff99;letter-spacing:3px;">
            CYBER<span style="color:#00e5ff;">SHIELD</span>
        </div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:8px;
                    color:#0a3020;letter-spacing:2px;margin-top:3px;">CONTROL PANEL</div>
    </div>
    """, unsafe_allow_html=True)

    # Protocol filter label
    st.markdown("""<div style="font-family:'Share Tech Mono',monospace;font-size:9px;
                color:#00ff9960;letter-spacing:4px;margin-bottom:6px;">// PROTOCOL FILTER</div>""",
                unsafe_allow_html=True)

    proto = st.selectbox(
        label="protocol",
        options=["5", "1", "2", "3", "4"],
        format_func=lambda x: {
            "5": "[ ALL ]  EVERYTHING",
            "1": "[ TCP ]  Transmission",
            "2": "[ UDP ]  Datagram",
            "3": "[ ICMP ] Control",
            "4": "[ HTTP ] HyperText",
        }[x],
        label_visibility="collapsed",
    )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.markdown("""<div style="font-family:'Share Tech Mono',monospace;font-size:9px;
                color:#00ff9960;letter-spacing:4px;margin-bottom:6px;">// ENGINE CONTROLS</div>""",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶ START", key="btn_start"):
            if (
                st.session_state.sniffer_process is None
                or not st.session_state.sniffer_process.is_alive()
            ):
                p = multiprocessing.Process(target=start_sniffing, args=(proto,))
                p.start()
                st.session_state.sniffer_process = p
                st.success("SNIFFER ACTIVE")
            else:
                st.warning("ALREADY RUNNING")

    with col2:
        if st.button("■ STOP", key="btn_stop"):
            if st.session_state.sniffer_process:
                st.session_state.sniffer_process.terminate()
                st.session_state.sniffer_process = None
                generate_text_report()
                st.error("SNIFFER STOPPED")
            else:
                st.info("NOTHING RUNNING")

    st.markdown("<hr style='border:none;border-top:1px solid #00ff9912;margin:12px 0;'>",
                unsafe_allow_html=True)

    # Status pill
    sn_color = "#00ff99" if is_running else "#ff3366"
    sn_label  = "RUNNING" if is_running else "IDLE"
    st.markdown(f"""
    <div style="background:#060f18;border:1px solid #00ff9918;border-radius:6px;
                padding:11px;text-align:center;margin-bottom:10px;">
        <div style="font-family:'Share Tech Mono',monospace;font-size:8px;
                    color:#0a4030;letter-spacing:3px;margin-bottom:5px;">SNIFFER STATUS</div>
        <div style="font-family:'Orbitron',sans-serif;font-size:14px;font-weight:700;
                    color:{sn_color};letter-spacing:3px;">&#9679; {sn_label}</div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    log_lines = 0
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            log_lines = sum(1 for _ in f)

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:10px;">
        <div style="background:#060f18;border:1px solid #00e5ff14;border-radius:6px;
                    padding:9px 7px;text-align:center;">
            <div style="font-family:'Orbitron',sans-serif;font-size:18px;
                        font-weight:700;color:#00ff99;">{log_lines}</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:8px;
                        color:#0a4040;letter-spacing:2px;margin-top:2px;">PACKETS</div>
        </div>
        <div style="background:#060f18;border:1px solid #00e5ff14;border-radius:6px;
                    padding:9px 7px;text-align:center;">
            <div style="font-family:'Orbitron',sans-serif;font-size:18px;
                        font-weight:700;color:#00e5ff;">—</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:8px;
                        color:#0a4040;letter-spacing:2px;margin-top:2px;">HOSTS</div>
        </div>
        <div style="background:#060f18;border:1px solid #ff336614;border-radius:6px;
                    padding:9px 7px;text-align:center;">
            <div style="font-family:'Orbitron',sans-serif;font-size:18px;
                        font-weight:700;color:#ff3366;">0</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:8px;
                        color:#4a1020;letter-spacing:2px;margin-top:2px;">ALERTS</div>
        </div>
        <div style="background:#060f18;border:1px solid #cc44ff14;border-radius:6px;
                    padding:9px 7px;text-align:center;">
            <div style="font-family:'Orbitron',sans-serif;font-size:18px;
                        font-weight:700;color:#cc44ff;">0</div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:8px;
                        color:#2a0a40;letter-spacing:2px;margin-top:2px;">KB/s</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Threat level
    threat_pct   = min(log_lines // 5, 100)
    threat_color = "#00ff99" if threat_pct < 25 else "#ff9900" if threat_pct < 60 else "#ff3366"
    threat_label = "LOW"    if threat_pct < 25 else "MEDIUM"  if threat_pct < 60 else "HIGH"
    st.markdown(f"""
    <div style="background:#060f18;border:1px solid #ff336614;border-radius:6px;
                padding:11px;margin-bottom:10px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
            <div style="font-family:'Share Tech Mono',monospace;font-size:8px;
                        color:#ff336650;letter-spacing:3px;">THREAT LEVEL</div>
            <div style="font-family:'Orbitron',sans-serif;font-size:11px;
                        color:{threat_color};letter-spacing:2px;">{threat_label}</div>
        </div>
        <div style="background:#0a0a0a;border-radius:2px;height:5px;overflow:hidden;">
            <div style="width:{max(threat_pct, 4)}%;height:5px;
                        background:linear-gradient(90deg,#00ff99,#00e5ff,{threat_color});
                        border-radius:2px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Log file info
    log_exists = os.path.exists(LOG_FILE)
    lf_color   = "#00ff99" if log_exists else "#ff3366"
    lf_label   = "FOUND"   if log_exists else "MISSING"
    st.markdown(f"""
    <div style="background:#060f18;border:1px solid #00ff9912;border-radius:6px;
                padding:10px 12px;">
        <div style="font-family:'Share Tech Mono',monospace;font-size:8px;
                    color:#0a4030;letter-spacing:3px;margin-bottom:7px;">// LOG FILE</div>
        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
            <span style="font-family:'Share Tech Mono',monospace;font-size:10px;color:#1a4030;">STATUS</span>
            <span style="font-family:'Share Tech Mono',monospace;font-size:10px;color:{lf_color};">&#9679; {lf_label}</span>
        </div>
        <div style="display:flex;justify-content:space-between;">
            <span style="font-family:'Share Tech Mono',monospace;font-size:10px;color:#1a4030;">ENTRIES</span>
            <span style="font-family:'Share Tech Mono',monospace;font-size:10px;color:#7fffd4;">{log_lines}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="position:absolute;bottom:14px;left:0;right:0;text-align:center;
                font-family:'Share Tech Mono',monospace;font-size:8px;
                color:#0a2018;letter-spacing:2px;">
        IMROHAIL 043 PROJECT &copy; 2025
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
#  MAIN — LIVE STREAM PANEL LABEL
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
    <div style="width:3px;height:16px;background:#00ff99;"></div>
    <span style="font-family:'Share Tech Mono',monospace;font-size:10px;
                 color:#00ff99;letter-spacing:4px;">LIVE PACKET STREAM</span>
    <div style="flex:1;height:1px;background:#00ff9912;"></div>
    <span style="font-family:'Share Tech Mono',monospace;font-size:8px;
                 color:#0a3020;letter-spacing:2px;">AUTO-REFRESH: 1s</span>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
#  LIVE TABLE PLACEHOLDER
# ──────────────────────────────────────────────────────────────────────────────
table_placeholder = st.empty()

# ──────────────────────────────────────────────────────────────────────────────
#  SECONDARY PANELS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

panel_col1, panel_col2 = st.columns(2)

with panel_col1:
    st.markdown("""
    <div style="background:#040b12;border:1px solid #00e5ff14;border-radius:6px;padding:12px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:9px;">
            <div style="width:3px;height:12px;background:#00e5ff;"></div>
            <span style="font-family:'Share Tech Mono',monospace;font-size:9px;
                         color:#00e5ff;letter-spacing:4px;">HEX STREAM</span>
        </div>
        <div style="font-family:'Share Tech Mono',monospace;font-size:9px;
                    color:#00e5ff28;letter-spacing:1px;line-height:1.9;">
            A4:F2 B1:9E 3C:AA FF:01 00:DE AD:BE EF:CA<br>
            12:34 56:78 90:AB CD:EF 01:23 45:67 89:01<br>
            67:89 AB:CD EF:01 23:45 67:89 0A:1B 2C:3D
        </div>
    </div>
    """, unsafe_allow_html=True)

with panel_col2:
    st.markdown("""
    <div style="background:#040b12;border:1px solid #cc44ff14;border-radius:6px;padding:12px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
            <div style="width:3px;height:12px;background:#cc44ff;"></div>
            <span style="font-family:'Share Tech Mono',monospace;font-size:9px;
                         color:#cc44ff;letter-spacing:4px;">PROTOCOL BREAKDOWN</span>
        </div>
        <div style="display:flex;flex-direction:column;gap:7px;
                    font-family:'Share Tech Mono',monospace;font-size:9px;">
            <div style="display:flex;align-items:center;gap:8px;">
                <span style="color:#00aaff;width:38px;">TCP</span>
                <div style="flex:1;background:#0a0a0a;border-radius:2px;height:5px;">
                    <div style="width:55%;height:5px;background:#00aaff;border-radius:2px;"></div>
                </div>
                <span style="color:#0a4040;width:28px;text-align:right;">55%</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <span style="color:#66dd00;width:38px;">UDP</span>
                <div style="flex:1;background:#0a0a0a;border-radius:2px;height:5px;">
                    <div style="width:25%;height:5px;background:#66dd00;border-radius:2px;"></div>
                </div>
                <span style="color:#0a4040;width:28px;text-align:right;">25%</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <span style="color:#ff9900;width:38px;">ICMP</span>
                <div style="flex:1;background:#0a0a0a;border-radius:2px;height:5px;">
                    <div style="width:12%;height:5px;background:#ff9900;border-radius:2px;"></div>
                </div>
                <span style="color:#0a4040;width:28px;text-align:right;">12%</span>
            </div>
            <div style="display:flex;align-items:center;gap:8px;">
                <span style="color:#cc44ff;width:38px;">HTTP</span>
                <div style="flex:1;background:#0a0a0a;border-radius:2px;height:5px;">
                    <div style="width:8%;height:5px;background:#cc44ff;border-radius:2px;"></div>
                </div>
                <span style="color:#0a4040;width:28px;text-align:right;">8%</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

# Report panel
st.markdown("""
<div style="background:#040b12;border:1px solid #ff336612;border-radius:6px;padding:12px;">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
        <div style="width:3px;height:12px;background:#ff3366;"></div>
        <span style="font-family:'Share Tech Mono',monospace;font-size:9px;
                     color:#ff3366;letter-spacing:4px;">REPORT GENERATOR</span>
    </div>
    <div style="font-family:'Share Tech Mono',monospace;font-size:10px;
                color:#2a1020;letter-spacing:1px;">
        Report auto-generated on STOP &nbsp;&#9670;&nbsp;
        Output: <span style="color:#ff336655;">data/reports/report.txt</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Ticker bar
st.markdown("""
<div style="background:#020608;border:1px solid #00ff9910;border-radius:4px;
            padding:7px 16px;margin-top:12px;overflow:hidden;white-space:nowrap;">
    <span style="font-family:'Share Tech Mono',monospace;font-size:9px;
                 color:#0a4030;letter-spacing:2px;">
        CYBER SHIELD ACTIVE &nbsp;&#9670;&nbsp; MONITORING NETWORK TRAFFIC &nbsp;&#9670;&nbsp;
        NO THREATS DETECTED &nbsp;&#9670;&nbsp; IMROHAIL 043 PROJECT &nbsp;&#9670;&nbsp;
        ALL SYSTEMS NOMINAL &nbsp;&#9670;&nbsp; PACKET ANALYSIS RUNNING &nbsp;&#9670;&nbsp;
        FIREWALL INTACT &nbsp;&#9670;&nbsp; ENCRYPTION LAYER OK &nbsp;&#9670;
    </span>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="background:#020608;border:1px solid #00ff9910;border-radius:6px;
            padding:9px 20px;margin-top:8px;display:flex;align-items:center;gap:10px;">
    <div style="width:6px;height:6px;border-radius:50%;background:#00ff99;flex-shrink:0;"></div>
    <span style="font-family:'Share Tech Mono',monospace;font-size:9px;
                 color:#0a3020;letter-spacing:2px;">CYBER SHIELD PRO</span>
    <span style="font-family:'Share Tech Mono',monospace;font-size:9px;
                 color:#0a3020;letter-spacing:2px;margin-left:auto;">
        DEVELOPED BY IMROHAIL 043 PROJECT &copy; 2025
    </span>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
#  REAL-TIME REFRESH LOOP  (original logic — unchanged)
# ──────────────────────────────────────────────────────────────────────────────
while True:
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()

        if lines:
            data = [
                {"TIME": time.strftime("%H:%M:%S"), "LOG ENTRY": l.strip()}
                for l in lines[-15:]
            ]
            df = pd.DataFrame(data)
            with table_placeholder.container():
                st.markdown("""
                <div style="background:#040b12;border:1px solid #00ff9918;
                            border-radius:6px;overflow:hidden;">
                """, unsafe_allow_html=True)
                st.table(df)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            with table_placeholder.container():
                st.markdown("""
                <div style="background:#040b12;border:1px solid #00ff9918;
                            border-radius:6px;padding:26px;text-align:center;
                            font-family:'Share Tech Mono',monospace;font-size:11px;
                            color:#0a3020;letter-spacing:3px;">
                    &#9675; &nbsp; AWAITING PACKETS — PRESS START TO BEGIN CAPTURE
                </div>
                """, unsafe_allow_html=True)
    else:
        with table_placeholder.container():
            st.markdown("""
            <div style="background:#0d0808;border:1px solid #ff336625;
                        border-radius:6px;padding:22px;text-align:center;
                        font-family:'Share Tech Mono',monospace;font-size:11px;
                        color:#aa2233;letter-spacing:2px;">
                &#10005; &nbsp; LOG FILE NOT FOUND &nbsp; | &nbsp; PATH: data/logs/network_log.txt
            </div>
            """, unsafe_allow_html=True)

    time.sleep(1)