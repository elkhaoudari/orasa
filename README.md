# ORASA — Offensive Security Recon & Attack Surface Analyzer


**ORASA** is a lightweight Offensive Security reconnaissance toolkit to help penetration testers, red teamers and security researchers quickly map attack surface for a target domain.


## Features
- Subdomain enumeration using crt.sh
- Basic HTTP header fingerprinting
- Simple TCP port scanner with banner grabbing
- Outputs JSON and HTML reports


## Quickstart
1. Clone repo
```bash
git clone https://github.com/<you>/orasa.git
cd orasa
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt