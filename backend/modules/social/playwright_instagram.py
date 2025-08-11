# modules/social/playwright_instagram.py
"""
Полноценный скрапинг Instagram с использованием Playwright + Stealth.
Обходит bot-детекторы, использует прокси и user-agent спуфинг.
"""

from playwright.async_api import async_playwright
import asyncio
import re
import logging

logger = logging.getLogger(__name__)

async def scrape_instagram_profile(username: str, proxy: str = None) -> dict:
    """
    Скрапинг профиля Instagram с обходом защиты.
    :param username: Имя пользователя Instagram
    :param proxy: Прокси в формате http://user:pass@ip:port (опционально)
    :return: Данные профиля
    """
    browser = None
    try:
        async with async_playwright() as p:
            # Настройка прокси
            browser_args = ["--disable-blink-features=AutomationControlled"]
            if proxy:
                browser_args.append(f"--proxy-server={proxy}")

            browser = await p.chromium.launch(
                headless=True,
                args=browser_args
            )

            context = await browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )

            # Убираем следы автоматизации
            await context.add_init_script("""
                () => {
                    Object.defineProperty(navigator, 'webdriver', { get: () => false });
                    window.chrome = { runtime: {} };
                    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
                    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                }
            """)

            page = await context.new_page()

            # Заходим на профиль
            url = f"https://www.instagram.com/{username}/"
            await page.goto(url, wait_until="networkidle", timeout=30000)

            # Пропускаем всплывающие окна (если залогинены)
            try:
                await page.wait_for_selector("button", timeout=5000)
                buttons = await page.query_selector_all("button")
                for btn in buttons:
                    txt = await btn.text_content()
                    if "отмена" in txt.lower() or "skip" in txt.lower():
                        await btn.click()
                        break
            except:
                pass

            # Извлечение данных
            full_name = await get_text(page, "h1")
            bio = await get_text(page, "h1 + div")
            posts = await get_number(page, "li:nth-child(1) > span")
            followers = await get_number_from_aria(page, "li:nth-child(2) a")
            following = await get_number_from_aria(page, "li:nth-child(3) a")
            is_private = await page.query_selector("h2:has-text('Этот аккаунт приватный')") is not None
            profile_pic = await page.get_attribute("img[alt*='Photo'][src*='https']", "src")

            await browser.close()

            return {
                "username": username,
                "full_name": full_name,
                "bio": bio,
                "posts": posts,
                "followers": followers,
                "following": following,
                "is_private": is_private,
                "profile_pic": profile_pic,
                "url": url
            }

    except Exception as e:
        logger.error(f"Ошибка при скрапинге Instagram ({username}): {e}")
        return {"error": str(e), "username": username}
    finally:
        if browser:
            await browser.close()


async def get_text(page, selector: str) -> str:
    try:
        el = await page.wait_for_selector(selector, timeout=10000)
        return (await el.text_content()).strip() if el else ""
    except:
        return ""


async def get_number(page, selector: str) -> int:
    text = await get_text(page, selector)
    return int(re.sub(r"[^\d]", "", text)) if text else 0


async def get_number_from_aria(page, selector: str) -> int:
    try:
        el = await page.wait_for_selector(selector, timeout=10000)
        aria_label = await el.get_attribute("aria-label")
        if aria_label:
            num = re.search(r"\d+", aria_label.replace(" ", ""))
            return int(num.group()) if num else 0
        return await get_number(page, "span")
    except:
        return 0


# === Пример использования ===
if __name__ == "__main__":
    result = asyncio.run(scrape_instagram_profile("instagram", proxy="http://user:pass@ip:port"))
    print(result)