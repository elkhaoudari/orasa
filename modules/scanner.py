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