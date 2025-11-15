# ORASA — Offensive Security Recon & Attack Surface Analyzer

> **مقدمة سريعة:**
> مشروع احترافي ومرتب لعرض مهاراتك في Offensive Security على GitHub و LinkedIn. هذا المستند يحتوي على: هيكلة المشروع، README جاهز للنشر، كود بداية (CLI)، موديولات أساسية (recon, scanner, report), تعليمات تثبيت، مثال على منشور LinkedIn، خطة تطوير وroadmap.

---

## ✅ أهداف المشروع

* بناء أداة CLI بلغة Python تقوم بـ Recon و Attack Surface Analysis.
* تنتج تقارير JSON و HTML احترافية.
* منظمة كمشروع مفتوح المصدر مع documentation ونمط برمجي واضح.

---

## 🔧 Tech stack

* Python 3.10+
* Modules: `requests`, `python-nmap` (optional), `beautifulsoup4`, `dnspython`, `aiohttp` (optional), `jinja2` (for HTML report), `tqdm`.

---

## 📁 هيكلة المشروع (Suggested)

```
orasa/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── orasa.py                # CLI entrypoint
├── modules/
│   ├── recon.py
│   ├── subdomains.py
│   ├── scanner.py
│   ├── report.py
│   └── utils.py
├── docs/
│   └── example_report.html
└── examples/
    └── sample_output.json
```

---

## 📄 README (Short preview)

(Full README included in this doc's "README.md" section below)

---

## 🧭 CLI - orasa.py (starter)

```python
#!/usr/bin/env python3
import argparse
from modules.recon import Recon
from modules.scanner import PortScanner
from modules.report import Report


def main():
    parser = argparse.ArgumentParser(prog='orasa', description='Offensive Security Recon & Attack Surface Analyzer')
    parser.add_argument('--domain', '-d', required=True, help='Target domain, e.g. example.com')
    parser.add_argument('--full-scan', action='store_true', help='Run full recon + port scan + report')
    parser.add_argument('--ports', '-p', default='1-1024', help='Port range (e.g. 1-1024 or 22,80,443)')
    parser.add_argument('--output', '-o', default='results.json', help='Output JSON file')
    args = parser.parse_args()

    recon = Recon(args.domain)
    recon.run_basic()

    if args.full_scan:
        scanner = PortScanner(args.domain, args.ports)
        scanner.run()
        recon.merge_ports(scanner.results)

    report = Report(recon.get_results())
    report.to_json(args.output)
    report.to_html('report.html')
    print(f'Finished. JSON -> {args.output}, HTML -> report.html')

if __name__ == '__main__':
    main()
```

---

## 🔍 modules/recon.py (starter)

```python
import requests
import re
from .subdomains import fetch_subdomains

class Recon:
    def __init__(self, domain):
        self.domain = domain
        self.data = {'domain': domain, 'subdomains': [], 'headers': {}, 'ports': []}

    def run_basic(self):
        self._fetch_headers()
        subs = fetch_subdomains(self.domain)
        self.data['subdomains'] = subs

    def _fetch_headers(self):
        try:
            r = requests.get(f'https://{self.domain}', timeout=8, allow_redirects=True)
            self.data['headers'] = dict(r.headers)
        except Exception:
            try:
                r = requests.get(f'http://{self.domain}', timeout=8)
                self.data['headers'] = dict(r.headers)
            except Exception:
                self.data['headers'] = {}

    def merge_ports(self, ports):
        self.data['ports'] = ports

    def get_results(self):
        return self.data
```

---

## 🌐 modules/subdomains.py (starter using crt.sh)

```python
import requests
import re

CRT_SH = 'https://crt.sh/?q=%25.{domain}&output=json'

def fetch_subdomains(domain):
    try:
        url = CRT_SH.format(domain=domain)
        r = requests.get(url, timeout=10)
        js = r.json()
        found = set()
        for item in js:
            name = item.get('name_value')
            for n in name.split('\n'):
                n = n.strip()
                if n.endswith(domain):
                    found.add(n)
        return sorted(found)
    except Exception:
        return []
```

---

## 🔌 modules/scanner.py (simple TCP port scanner)

```python
import socket
from concurrent.futures import ThreadPoolExecutor

class PortScanner:
    def __init__(self, host, ports='1-1024'):
        self.host = host
        self.ports = self._parse_ports(ports)
        self.results = []

    def _parse_ports(self, ports_str):
        if '-' in ports_str:
            a, b = ports_str.split('-')
            return list(range(int(a), int(b) + 1))
        else:
            return [int(p.strip()) for p in ports_str.split(',') if p.strip()]

    def _scan_port(self, port):
        try:
            s = socket.socket()
            s.settimeout(1.0)
            s.connect((self.host, port))
            try:
                banner = s.recv(1024).decode(errors='ignore').strip()
            except Exception:
                banner = ''
            s.close()
            return {'port': port, 'open': True, 'banner': banner}
        except Exception:
            return {'port': port, 'open': False}

    def run(self, workers=100):
        with ThreadPoolExecutor(max_workers=workers) as ex:
            for res in ex.map(self._scan_port, self.ports):
                if res.get('open'):
                    self.results.append(res)
```

---

## 📑 modules/report.py (JSON + simple HTML using jinja2)

```python
import json
from jinja2 import Template

HTML_TMPL = """
<html>
<head><meta charset='utf-8'><title>ORASA Report - {{domain}}</title></head>
<body>
<h1>ORASA Report — {{domain}}</h1>
<h2>Subdomains</h2>
<ul>{% for s in subdomains %}<li>{{s}}</li>{% endfor %}</ul>
<h2>Headers</h2>
<pre>{{ headers }}</pre>
<h2>Open Ports</h2>
<ul>{% for p in ports %}<li>{{p.port}} — {{p.banner}}</li>{% endfor %}</ul>
</body>
</html>
"""

class Report:
    def __init__(self, data):
        self.data = data

    def to_json(self, filename='results.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def to_html(self, filename='report.html'):
        tpl = Template(HTML_TMPL)
        html = tpl.render(domain=self.data.get('domain'), subdomains=self.data.get('subdomains', []), headers=self.data.get('headers', {}), ports=self.data.get('ports', []))
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
```

---

## 📦 requirements.txt

```
requests
beautifulsoup4
jinja2
dnspython
python-nmap
tqdm
```

---

## 📝 README.md (Full - ready to drop in GitHub)

````markdown
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
````

2. Run

```bash
python3 orasa.py -d example.com --full-scan -p 1-1024 -o example_results.json
```

## Roadmap

* Add async scanners (aiohttp)
* Integrate Amass-like passive sources
* Add vulnerability checks (CSP, HSTS, clickjacking)
* Add HTML dashboard and screenshots with puppeteer

## License

MIT — see LICENSE

```

---

## ✍️ LinkedIn Post Template (Arabic/English mix)
```

🚀 Released: ORASA — Offensive Security Recon & Attack Surface Analyzer

Today I published ORASA, a lightweight recon toolkit I built to map attack surfaces and speed up reconnaissance tasks. The tool performs subdomain enumeration, header fingerprinting, port scanning and produces JSON/HTML reports.

Why I built it:

* To practise offensive security workflows
* To create a shareable, extensible project that shows technical depth

GitHub: [https://github.com/](https://github.com/)<your-username>/orasa

Feedback welcome — issues, PRs and stars appreciated!

```

---

## 🧭 First commits & git strategy (suggested)
1. `feat: initial project structure and README`
2. `feat: add recon module (crt.sh)`
3. `feat: add port scanner`
4. `chore: add report generator and example report`

---

## 🎯 Next steps for you (as a beginner)
1. Clone the repo and run `orasa.py` on a domain you own or have permission to test.
2. Read each module file, run it line-by-line and add print/debug statements to understand the flow.
3. Try to add one improvement: e.g., save screenshots, add retry logic, or increase scanner speed safely.

---

## 📌 Ethics & Legal
**Never** run ORASA without explicit permission on targets you do not own. Use this for learning, lab targets and authorized engagements only.

---


---

*End of document.*

```
