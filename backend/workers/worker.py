# workers/worker.py
from celery import Celery
from core.engine import SpiderEngine
import asyncio
from .telegram_bot import notify_telegram, start_bot

# Запуск бота при старте Celery
@celery.task
def start_telegram_bot():
    start_bot()

celery = Celery('spider_tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@celery.task
def run_osint_scan(target: str, modules: list, report: bool):
    engine = SpiderEngine(target=target, modules=modules)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(engine.run())
    if report:
        engine.generate_report(engine.results)
    return {"status": "completed", "target": target}