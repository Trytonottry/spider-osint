from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
from workers.telegram_bot import notify_telegram
from db.saver import save_scan_result
import json
from fastapi import APIRouter
from db.database import SessionLocal
from db.models import Target, ScanResult

router = APIRouter()

@router.get("/history/{target}")
def get_scan_history(target: str):
    db = SessionLocal()
    db_target = db.query(Target).filter(Target.value == target).first()
    if not db_target:
        return {"scans": []}
    
    scans = []
    for result in db_target.results:
        scans.append({
            "timestamp": result.timestamp,
            "modules": result.modules_used.split(","),
            "suspicious": result.suspicious,
            "report_pdf": result.report_pdf,
            "data_preview": dict(list(result.data.items())[:5])  # только часть
        })
    db.close()
    return {"target": target, "scans": scans}

app.include_router(router, prefix="/api")

app = FastAPI(title="SPIDER OSINT API", 
              version="7.1",
              description="API для автоматизации OSINT-исследований с ИИ",
              docs_url="/docs",
              redoc_url="/redoc")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class ScanRequest(BaseModel):
    target: str
    modules: list = ["all"]
    generate_report: bool = True

@app.post("/scan")
async def start_scan(request: ScanRequest):
    # Здесь можно добавить Celery задачу
    # Пока упрощённо
    result = {"status": "completed", "target": request.target}
    save_scan_result(request.target, request.modules, result)
    if request.generate_report:
        notify_telegram.delay(f"Scan completed: {request.target}")
    return result

@app.get("/api/history/{target}")
def get_history(target: str):
    from db.database import SessionLocal
    from db.models import Target, ScanResult
    db = SessionLocal()
    t = db.query(Target).filter(Target.value == target).first()
    if not t:
        return {"scans": []}
    return {
        "target": t.value,
        "scans": [
            {
                "timestamp": s.timestamp,
                "modules": s.modules_used.split(","),
                "suspicious": s.suspicious
            } for s in t.results
        ]
    }

@app.post("/ask")
async def ask_assistant(query: str, context: str):
    assistant = OSINTAssistant()
    answer = assistant.ask(query, context)
    return {"answer": answer}

app.include_router(router, prefix="/api")