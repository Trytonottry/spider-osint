# utils/source_router.py
from typing import List

ROUTING_TABLE = {
    "email": ["social", "web", "files", "breach"],
    "domain": ["web", "network", "dns", "phishing", "shodan"],
    "ip": ["network", "shodan", "censys", "web"],
    "username": ["social", "web"],
    "phone": ["web", "social", "numverify"],
    "hash": ["virustotal", "hybrid"]
}

def get_modules_for_target(target: str) -> List[str]:
    from utils.target_type import classify_target
    target_type = classify_target(target)
    return ROUTING_TABLE.get(target_type, ["web"])