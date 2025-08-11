# reports/demo.py
def generate_demo_report():
    demo_data = {
        "target": "demo@spider.osint",
        "type": "email",
        "social": {
            "vk": [{"id": 123, "name": "Иван Иванов", "city": "Москва"}],
            "twitter": [{"handle": "@ivan_fake", "bio": "Security researcher"}]
        },
        "ai": {
            "sentiment": "neutral",
            "entities": [{"text": "Москва", "type": "GPE"}],
            "summary": "Пользователь из Москвы, интересуется безопасностью."
        },
        "graph": {"nodes": 5, "edges": 7}
    }
    gen = ReportGenerator(demo_data)
    gen.generate_pdf("demo_report.pdf")
    gen.generate_html("demo_report.html")