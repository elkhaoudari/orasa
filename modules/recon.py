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