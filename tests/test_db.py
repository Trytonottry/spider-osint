# tests/test_db.py
from db.database import init_db, engine
from db.models import Base

def test_db_creation():
    Base.metadata.create_all(bind=engine)
    assert True