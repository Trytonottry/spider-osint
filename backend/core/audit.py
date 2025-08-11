# core/audit.py
import logging
from datetime import datetime
import json

audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/audit.log")
formatter = logging.Formatter('%(asctime)s | %(user)s | %(action)s | %(target)s | %(ip)s')
handler.setFormatter(formatter)
audit_logger.addHandler(handler)

def log_action(user: str, action: str, target: str = None, ip: str = None):
    audit_logger.info("", extra={
        "user": user,
        "action": action,
        "target": target,
        "ip": ip
    })