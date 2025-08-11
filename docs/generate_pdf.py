# docs/generate_pdf.py
from weasyprint import HTML
import markdown

def generate_pdf():
    with open("docs/ARCHITECTURE.md") as f:
        html = markdown.markdown(f.read())
    HTML(string=html).write_pdf("SPIDER_Technical_Documentation_v6.0.pdf")

if __name__ == "__main__":
    generate_pdf()