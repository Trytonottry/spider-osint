# modules/web/gather.py
from .playwright_scraper import scrape_with_stealth

async def gather(target: str) -> dict:
    results = {}
    url = f"https://google.com/search?q={target}"
    try:
        content = await scrape_with_stealth(url)
        results["google"] = content[:1000]  # Упрощённо
    except Exception as e:
        results["error"] = str(e)
    return results