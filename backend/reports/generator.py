# reports/generator.py
from jinja2 import Template
from weasyprint import HTML
import json

class ReportGenerator:
    def __init__(self,  dict):
        self.data = data
        self.template_html = """
        <h1>OSINT Report — {{ target }}</h1>
        <h2>Results</h2>
        <pre>{{ data | tojson(indent=2) }}</pre>
        """

    def generate_html(self, filename: str):
        template = Template(self.template_html)
        html_out = template.render(target="Target", data=self.data)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_out)
        print(f"[+] HTML report saved: {filename}")

    def generate_pdf(self, filename: str):
        self.generate_html("temp_report.html")
        HTML("temp_report.html").write_pdf(filename)
        print(f"[+] PDF report saved: {filename}")