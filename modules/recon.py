import socket
import requests

class Recon:
    def __init__(self, domain):
        self.domain = domain
        self.results = {
            "domain": domain,
            "ip": "",
            "headers": {},
            "open_ports": []
        }

    def run_basic(self):
        # Resolve IP
        try:
            ip = socket.gethostbyname(self.domain)
            self.results["ip"] = ip
        except Exception as e:
            self.results["ip"] = f"Error: {e}"

        # Get HTTP headers
        try:
            r = requests.get(f"http://{self.domain}", timeout=5)
            self.results["headers"] = dict(r.headers)
        except:
            self.results["headers"] = {"error": "Could not fetch headers"}

    def merge_ports(self, ports):
        self.results["open_ports"] = ports

    def get_results(self):
        return self.results
