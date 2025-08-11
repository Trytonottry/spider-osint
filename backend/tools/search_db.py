# tools/search_db.py
from db.database import SessionLocal
from db.models import Target, ScanResult

def search_target(value: str):
    db = SessionLocal()
    target = db.query(Target).filter(Target.value.ilike(f"%{value}%")).first()
    if target:
        print(f"🎯 Найдено: {target.value} (тип: {target.type})")
        for result in target.results:
            print(f"  📅 {result.timestamp} | Модули: {result.modules_used}")
    else:
        print("❌ Цель не найдена в базе")
    db.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        search_target(sys.argv[1])
    else:
        print("Использование: python search_db.py email@example.com")