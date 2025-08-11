# modules/web/playwright_scraper.py
from playwright.async_api import async_playwright
import asyncio

async def scrape_with_stealth(url: str, proxy: str = None) -> str:
    async with async_playwright() as p:
        browser_args = ["--disable-blink-features=AutomationControlled"]
        if proxy:
            browser_args.append(f"--proxy-server={proxy}")

        browser = await p.chromium.launch(headless=True, args=browser_args)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            viewport={"width": 1920, "height": 1080},
            java_script_enabled=True
        )

        # Убираем следы автоматизации
        await context.add_init_script("""
            () => {
                Object.defineProperty(navigator, 'webdriver', { get: () => false });
                window.chrome = { runtime: {} };
                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
            }
        """)

        page = await context.new_page()
        await page.goto(url, wait_until="networkidle", timeout=30000)
        content = await page.evaluate("document.body.innerHTML")
        await browser.close()
        return content