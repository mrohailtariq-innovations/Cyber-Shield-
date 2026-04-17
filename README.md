
```markdown
<p align="center">
  <img src="https://capsule-render.vercel.app/render?type=soft&color=red&hasPattern=true&height=300&section=header&text=Packet%20Safar&fontSize=90&animation=fadeIn" alt="header" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Security-IDS-red?style=for-the-badge&logo=fortinet&logoColor=white" />
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
</p>

---

## 🛡️ Introduction
**Packet Safar (پیکٹ سفر)** is a professional-grade Network Packet Sniffer and Intrusion Detection System (IDS). It provides a deep-dive journey into your network traffic, allowing you to monitor, analyze, and secure your local environment through a sleek, real-time Web Dashboard.

> "Every packet tells a story. We help you read it."

---

## ✨ Features

### 📡 1. Real-Time Packet Sniffing
* **Deep Inspection:** Capture and analyze IP, TCP, UDP, and ICMP layers.
* **Modular Engine:** Built with Scapy for high-performance packet manipulation.
* **Smart Filtering:** Filter traffic based on specific protocols or target IPs.

### 🚨 2. Intelligent Detection (IDS)
* **Signature-Based Alerts:** Automatically detects suspicious port activity (e.g., 4444, 8080).
* **Visual Alerts:** Real-time RED alerts on the dashboard when a threat is detected.
* **Automated Logging:** Saves every suspicious attempt for forensic audit.

### 📊 3. Pro Dashboard & Reporting
* **Streamlit UI:** Control the entire sniffer (Start/Stop) from a web browser.
* **Multi-Process Architecture:** Sniffer and UI run on separate cores for 0% lag.
* **PDF/Text Reports:** Generates a comprehensive summary of network health upon exit.

---

## 🚀 Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python / Scapy Engine |
| **Frontend** | Streamlit Web Framework |
| **Logic** | Multiprocessing & BPF Filtering |
| **Storage** | Raw Text Logging & Pandas Analysis |

---

## 📂 Project Structure

```text
PacketSafar/
├── frontend/
│   └── app.py             # The Master Dashboard UI
├── backend/
│   ├── sniffer.py         # Core Sniffing Logic
│   └── __init__.py
├── detection/
│   ├── detector.py        # Threat Detection Engine
├── reporting/
│   └── report_generator.py # Summary Report Logic
├── data/
│   ├── logs/              # History of captured packets
│   └── reports/           # Final generated audits
└── requirements.txt       # Project Dependencies

```
## 🛠️ Step-by-Step Installation Guide
### Step 1: Clone the Repository
```bash
git clone [https://github.com/yourusername/PacketSafar.git](https://github.com/yourusername/PacketSafar.git)
cd PacketSafar

```
### Step 2: Install Drivers (Windows Only)
Install **Npcap**. Ensure you check the box: *"Install Npcap in WinPcap API-compatible Mode"*.
### Step 3: Install Dependencies
```bash
python -m pip install -r requirements.txt

```
### Step 4: Launch the Dashboard
```bash
python -m streamlit run frontend/app.py

```
## 💻 How It Works (The Logic)
 1. **The Core:** The Python backend uses the Scapy library to hook into your Network Interface Card (NIC).
 2. **The Filter:** It uses **BPF (Berkeley Packet Filters)** to ignore unnecessary traffic and focus on what matters.
 3. **The Detector:** Every packet is passed through detector.py. If a packet hits a "Suspicious Port," a red alert signal is sent.
 4. **The UI:** Streamlit acts as the "Observer." It reads the live logs every second and displays them in a clean table format.
## 👤 Author
**Muhammad Rohail**
*BSc Digital Forensics & Cybersecurity Student*
<p align="left">
<a href="https://github.com/yourusername"><img src="https://www.google.com/search?q=https://img.shields.io/badge/GitHub-100000%3Fstyle%3Dfor-the-badge%26logo%3Dgithub%26logoColor%3Dwhite" /></a>
<a href="https://linkedin.com/in/yourprofile"><img src="https://www.google.com/search?q=https://img.shields.io/badge/LinkedIn-0077B5%3Fstyle%3Dfor-the-badge%26logo%3Dlinkedin%26logoColor%3Dwhite" /></a>
</p>
<p align="center"> 🛡️ Secured with Packet Safar. </p>
```

