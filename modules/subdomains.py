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