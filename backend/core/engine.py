# core/engine.py
import os
import self
import asyncio
from typing import Dict, Any
from utils.logger import logger
from modules import social, web, network, images, files
from ai import nlp, vision, clustering
from reports.generator import ReportGenerator

from utils.target_type import classify_target
from utils.source_router import get_modules_for_target

from ai.ioc_extractor import IOCExtractor

from db.saver import save_scan_result
from db.database import SessionLocal
from db.models import ScanResult
from utils.diff import compare_results
from ai.assistant import OSINTAssistant

async def run(self):
    ...
    # Получаем последний результат
    last_result = None
    db = SessionLocal()
    latest_scan = db.query(ScanResult)\
        .join(Target)\
        .filter(Target.value == self.target)\
        .order_by(ScanResult.timestamp.desc())\
        .first()
    
    if latest_scan:
        last_result = json.loads(latest_scan.data)
    db.close()

    # Запускаем анализ
    self.results = await self.collect_data()
    await self.ai_enhance()

    # Сравниваем
    if last_result:
        diff = compare_results(last_result, self.results)
        self.results["changes"] = diff
        if diff:
            self.results["ai"]["alert"] = "Обнаружены изменения с последнего сканирования"
            # Уведомляем через Telegram
            notify_telegram.delay(f"⚠️ Изменения в {self.target}: {list(diff.keys())}")

class SpiderEngine:
    async def run(self) -> Dict[str, Any]:
        ...
        # После сбора данных
        self.results = await asyncio.gather(*tasks, return_exceptions=True)

        await self.ai_enhance()

        # 🔽 Сохраняем в PostgreSQL
        save_scan_result(
            target=self.target,
            modules=self.modules,
            data=self.results,
            report_pdf="reports/report.pdf" if self.args.report else None,
            report_html="reports/report.html" if self.args.report else None
        )

        return self.results

# После сбора данных
text = " ".join([str(v) for v in self.results.values()])
iocs = IOCExtractor().extract(text)
self.results["iocs"] = iocs

# Отправка в MISP
if os.getenv("AUTO_SEND_TO_MISP"):
    send_iocs_to_misp.delay(iocs)

class SpiderEngine:
    def __init__(self, target: str, modules: list = None):
        self.target = target
        self.modules = modules or get_modules_for_target(target)

class SpiderEngine:
    def __init__(self, target: str, modules: list = None):
        self.target = target
        self.target_type = classify_target(target)
        self.modules = modules or self.get_default_modules()

    def get_default_modules(self) -> list:
        mapping = {
            "email": ["social", "web", "files"],
            "domain": ["web", "network", "phishing"],
            "ip": ["network", "shodan", "web"],
            "username": ["social"],
            "phone": ["social", "web"],
        }
        return mapping.get(self.target_type, ["web", "social"])

class SpiderEngine:
    def __init__(self, target: str, modules: list):
        self.target = target
        self.modules = modules
        self.results = {}

    async def run(self) -> Dict[str, Any]:
        logger.info(f"Starting OSINT for target: {self.target}")
        tasks = []

        if "all" in self.modules or "social" in self.modules:
            tasks.append(self.run_module("social", social.gather(self.target)))
        if "all" in self.modules or "web" in self.modules:
            tasks.append(self.run_module("web", web.gather(self.target)))
        if "all" in self.modules or "network" in self.modules:
            tasks.append(self.run_module("network", network.gather(self.target)))
        if "all" in self.modules or "images" in self.modules:
            tasks.append(self.run_module("images", images.gather(self.target)))
        if "all" in self.modules or "files" in self.modules:
            tasks.append(self.run_module("files", files.gather(self.target)))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        for res in results:
            if isinstance(res, dict):
                self.results.update(res)

        # AI Processing
        await self.ai_enhance()

        return self.results

    async def run_module(self, name: str, coro):
        try:
            result = await coro
            logger.info(f"Module {name} completed")
            return {name: result}
        except Exception as e:
            logger.error(f"Module {name} failed: {e}")
            return {name: {"error": str(e)}}

    async def ai_enhance(self):
        text = " ".join([
            self.results.get("social", {}).get("bio", ""),
            self.results.get("web", {}).get("content", "")
        ])
        if text.strip():
            self.results["ai"] = {
                "nlp": nlp.analyze(text),
                "entities": nlp.extract_entities(text),
                "sentiment": nlp.sentiment(text),
                "summary": nlp.summarize(text)
            }

        # Vision AI (if images found)
        if "images" in self.results:
            faces = vision.detect_faces(self.results["images"].get("urls", []))
            self.results["ai"]["vision"] = {"faces": faces}

        # Clustering / Graph
        self.results["graph"] = clustering.build_graph(self.results)

    def generate_report(self, data):
        generator = ReportGenerator(data)
        generator.generate_pdf("spider_report.pdf")
        generator.generate_html("spider_report.html")
        logger.info("Report generated: spider_report.pdf, spider_report.html")