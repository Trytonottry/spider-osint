# db/saver.py
from db.database import SessionLocal
from db.models import Target, ScanResult
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json

def save_scan_result(target: str, modules: list,  dict, report_pdf: str = None, report_html: str = None):
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже такая цель
        db_target = db.query(Target).filter(Target.value == target).first()
        if not db_target:
            db_target = Target(value=target, type=infer_target_type(target))
            db.add(db_target)
            db.commit()
            db.refresh(db_target)

        # Обновляем время последнего сканирования
        db_target.last_scanned = datetime.utcnow()

        # Создаём результат
        scan_result = ScanResult(
            target_id=db_target.id,
            modules_used=",".join(modules),
            data=json.dumps(data, ensure_ascii=False, indent=2),
            report_pdf=report_pdf,
            report_html=report_html,
            suspicious=data.get("phishing", {}).get("risk_score", 0) > 50 or False
        )
        db.add(scan_result)
        db.commit()
        print(f"[DB] Результат сохранён для {target}")
    except IntegrityError:
        db.rollback()
        print(f"[DB] Ошибка сохранения для {target}")
    finally:
        db.close()

def infer_target_type(target: str) -> str:
    # Можно использовать уже готовую функцию из utils/target_type.py
    from utils.target_type import classify_target
    return classify_target(target)