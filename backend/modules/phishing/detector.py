# modules/phishing/detector.py
import tldextract
import re
from urllib.parse import urlparse

PHISHING_KEYWORDS = ["login", "secure", "account", "verify", "update", "paypal", "bank"]

def analyze_domain(domain: str) -> dict:
    ext = tldextract.extract(domain)
    score = 0
    warnings = []

    # 1. Подозрительные TLD
    if ext.suffix in ["xyz", "top", "click", "biz"]:
        score += 20
        warnings.append("Надёжный TLD")

    # 2. Длина домена
    if len(ext.domain) > 15:
        score += 15
        warnings.append("Длинное имя домена")

    # 3. Поддомен с ключевыми словами
    if any(kw in ext.subdomain for kw in PHISHING_KEYWORDS):
        score += 30
        warnings.append("Поддомен содержит 'login', 'secure' и т.д.")

    # 4. Похожесть на известные бренды
    brand_phishing = ["g00gle", "paypa1", "m1crosoft"]
    if any(b in domain for b in brand_phishing):
        score += 40
        warnings.append("Подмена бренда (typosquatting)")

    return {
        "domain": domain,
        "risk_score": min(score, 100),
        "suspicious": score >= 50,
        "warnings": warnings
    }