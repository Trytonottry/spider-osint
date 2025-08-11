# core/updater.py
import subprocess
import os

def update_modules():
    """Обновляет модули из удалённого репозитория"""
    if os.path.exists("modules"):
        subprocess.run(["git", "-C", "modules", "pull"], check=False)
    else:
        subprocess.run(["git", "clone", "https://github.com/spider-osint/modules.git"], check=False)