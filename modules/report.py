import json

class Report:
    def __init__(self, results):
        self.results = results

    def to_json(self, filename):
        with open(filename, "w") as f:
            json.dump(self.results, f, indent=4)

    def to_html(self, filename):
        html = f"""
        <html>
        <head><title>ORASA Report</title></head>
        <body>
            <h1>ORASA - Attack Surface Report</h1>
            <h2>Domain: {self.results['domain']}</h2>
            <h3>IP: {self.results['ip']}</h3>

            <h3>Open Ports:</h3>
            <ul>
                {''.join([f'<li>{p}</li>' for p in self.results['open_ports']])}
            </ul>

            <h3>Headers:</h3>
            <ul>
                {''.join([f'<li>{k}: {v}</li>' for k, v in self.results['headers'].items()])}
            </ul>
        </body>
        </html>
        """

        with open(filename, "w") as f:
            f.write(html)
