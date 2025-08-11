# tests/test_core.py
def test_engine_initialization():
    from core.engine import SpiderEngine
    engine = SpiderEngine(target="test@example.com", modules=["web"])
    assert engine.target == "test@example.com"