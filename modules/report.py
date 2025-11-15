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