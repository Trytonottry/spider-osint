# workers/monitor.py
from celery import Celery
import asyncio
from datetime import timedelta
from core.engine import SpiderEngine

celery = Celery('spider_tasks', broker='redis://redis:6379/0')

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Ежедневный мониторинг
    sender.add_periodic_task(
        crontab(hour=9, minute=0),  # Каждый день в 9:00
        run_monitoring.s()
    )

@celery.task
def run_monitoring():
    targets = ["ceo@company.com", "api.company.com", "192.168.1.1"]
    for target in targets:
        engine = SpiderEngine(target=target, modules=["all"])
        loop = asyncio.get_event_loop()
        loop.run_until_complete(engine.run())
        engine.generate_report(engine.results)
        notify_telegram.delay(f"Мониторинг завершён: {target}")