# utils/target_type.py
import re

def classify_target(target: str) -> str:
    target = target.strip().lower()

    if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", target):
        return "email"
    elif re.match(r"^https?://", target) or re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", target):
        return "domain"
    elif re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target):
        return "ip"
    elif re.match(r"^@[a-zA-Z0-9_]{1,15}$", target):  # Twitter
        return "username"
    elif re.match(r"^\+?[\d\s\-\(\)]{7,}$", target):
        return "phone"
    else:
        return "unknown"