# ai/ioc_extractor.py
import re
from typing import Dict, List

class IOCExtractor:
    patterns = {
        "ip": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "email": r"\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b",
        "domain": r"\b[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b",
        "url": r"https?://[^\s]+",
        "md5": r"\b[a-fA-F0-9]{32}\b",
        "sha256": r"\b[a-fA-F0-9]{64}\b"
    }

    def extract(self, text: str) -> Dict[str, List[str]]:
        iocs = {}
        for type_, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            # Фильтр: не домены вроде "google.com" из легальных источников
            if type_ == "domain":
                matches = [m for m in matches if len(m) > 4]
            iocs[type_] = list(set(matches))
        return iocs