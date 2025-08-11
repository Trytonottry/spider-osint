# api/export.py
from fastapi import APIRouter, Response
import csv
import json
from io import StringIO
from db.database import SessionLocal
from db.models import ScanResult

router = APIRouter()

@router.get("/export/{target}/csv")
def export_csv(target: str):
    db = SessionLocal()
    scans = db.query(ScanResult).join(Target).filter(Target.value == target).all()
    db.close()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Дата", "Модули", "Риски", "Отчёт PDF"])

    for scan in scans:
        writer.writerow([
            scan.timestamp,
            scan.modules_used,
            "Да" if scan.suspicious else "Нет",
            scan.report_pdf or ""
        ])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={target}_export.csv"}
    )

@router.get("/export/{target}/json")
def export_json(target: str):
    db = SessionLocal()
    scans = db.query(ScanResult).join(Target).filter(Target.value == target).all()
    db.close()

    data = []
    for scan in scans:
        data.append({
            "timestamp": scan.timestamp.isoformat(),
            "modules": scan.modules_used.split(","),
            "suspicious": scan.suspicious,
            "report_pdf": scan.report_pdf,
            "data": scan.data
        })

    return Response(
        content=json.dumps(data, ensure_ascii=False, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={target}_export.json"}
    )