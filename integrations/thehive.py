# integrations/thehive.py
import requests

def create_alert(thehive_url: str, api_key: str, title: str, description: str):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"title": title, "description": description, "type": "osint"}
    requests.post(f"{thehive_url}/api/alert", json=data, headers=headers)