import socket

class PortScanner:
    def __init__(self, domain, ports):
        self.domain = domain
        self.ports = self.parse_ports(ports)
        self.results = []

    def parse_ports(self, ports):
        if "-" in ports:
            start, end = ports.split("-")
            return range(int(start), int(end) + 1)
        else:
            return [int(p) for p in ports.split(",")]

    def scan_port(self, port):
        try:
            sock = socket.socket()
            sock.settimeout(0.5)
            sock.connect((self.domain, port))
            sock.close()
            return True
        except:
            return False

    def run(self):
        for port in self.ports:
            if self.scan_port(port):
                self.results.append(port)
