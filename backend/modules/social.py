# modules/social.py
"""
Модуль для сбора данных из социальных сетей.
Поддержка: VK, Telegram, Twitter/X, Instagram (ограниченно)
Использует API и Playwright для обхода защиты.
"""

import asyncio
import aiohttp
import re
from typing import Dict, List, Optional
from urllib.parse import quote

from utils.logger import logger
from utils.proxy import get_session
from ai.nlp import extract_entities, sentiment
from .playwright_instagram import scrape_instagram_profile as scrape_instagram


# =================== КОНФИГУРАЦИЯ ===================

# API Keys (должны быть в .env)
VK_ACCESS_TOKEN = "your_vk_token"  # Заменить на загрузку из .env
TWITTER_BEARER_TOKEN = "your_twitter_bearer"  # Используется для Twitter API v2

# User-Agent
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


# =================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ===================

def extract_username_from_url(url: str) -> Optional[str]:
    """Извлекает username из URL (например, t.me/username)"""
    patterns = [
        r"t\.me/([^/\s]+)",
        r"twitter\.com/([^/\s]+)",
        r"vk\.com/([^/\s]+)",
        r"instagram\.com/([^/\s]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


async def fetch_json(session: aiohttp.ClientSession, url: str, **kwargs) -> Dict:
    """Безопасный JSON-запрос"""
    try:
        async with session.get(url, **kwargs) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                logger.warning(f"HTTP {resp.status} при запросе {url}")
                return {}
    except Exception as e:
        logger.error(f"Ошибка при запросе {url}: {e}")
        return {}


# =================== VK (Vkontakte) ===================

async def search_vk_by_name(session: aiohttp.ClientSession, name: str) -> List[Dict]:
    """Поиск пользователей в VK по имени"""
    url = "https://api.vk.com/method/users.search"
    params = {
        "q": name,
        "access_token": VK_ACCESS_TOKEN,
        "v": "5.131",
        "count": 10,
        "fields": "photo_100,city,country,online,followers_count"
    }
    data = await fetch_json(session, url, params=params)
    return data.get("response", {}).get("items", [])


async def get_vk_profile(session: aiohttp.ClientSession, uid: int) -> Dict:
    """Получение профиля VK по ID"""
    url = "https://api.vk.com/method/users.get"
    params = {
        "user_ids": uid,
        "access_token": VK_ACCESS_TOKEN,
        "v": "5.131",
        "fields": "about,activities,bdate,contacts,education,interests"
    }
    data = await fetch_json(session, url, params=params)
    return data.get("response", [{}])[0]


# =================== TELEGRAM ===================

async def search_telegram(session: aiohttp.ClientSession, query: str) -> List[Dict]:
    """
    Поиск в Telegram через веб-интерфейс (ограниченно)
    В реальности лучше использовать Telethon (требует номер телефона)
    Здесь — пример поиска через t.me/s/
    """
    url = f"https://t.me/s/{quote(query)}"
    try:
        async with session.get(url, headers=HEADERS) as resp:
            if resp.status == 200:
                text = await resp.text()
                # Извлечение информации (упрощённо)
                matches = re.findall(r'class="tgme_channel_info_description">(.+?)</div>', text, re.DOTALL)
                description = matches[0].strip() if matches else ""
                return [{
                    "username": query,
                    "type": "channel" if "joinchat" not in text else "private",
                    "description": description[:500],
                    "url": f"https://t.me/{query}"
                }]
            return []
    except Exception as e:
        logger.error(f"Ошибка при поиске в Telegram: {e}")
        return []


# =================== TWITTER/X ===================

async def search_twitter(session: aiohttp.ClientSession, query: str) -> List[Dict]:
    """Поиск пользователей в Twitter через API v2"""
    url = "https://api.twitter.com/2/users/by/username/" + quote(query)
    headers = {
        **HEADERS,
        "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"
    }
    data = await fetch_json(session, url, headers=headers)
    user = data.get("data", {})
    if user:
        return [{
            "id": user.get("id"),
            "username": user.get("username"),
            "name": user.get("name"),
            "description": user.get("description"),
            "verified": user.get("verified", False),
            "public_metrics": user.get("public_metrics", {}),
            "url": f"https://twitter.com/{user.get('username')}"
        }]
    return []


async def search_twitter_by_name(session: aiohttp.ClientSession, name: str) -> List[Dict]:
    """Поиск по имени (не username)"""
    url = "https://api.twitter.com/2/users/by"
    params = {
        "usernames": name,
        "user.fields": "description,public_metrics,verified,created_at"
    }
    headers = {
        **HEADERS,
        "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"
    }
    return await fetch_json(session, url, headers=headers, params=params)


# =================== INSTAGRAM (через веб-скрапинг) ===================

async def scrape_instagram_profile(session: aiohttp.ClientSession, username: str) -> Dict:
    """
    Упрощённый скрапинг профиля Instagram
    Внимание: Instagram активно блокирует ботов.
    В реальности используйте playwright + stealth.
    """
    url = f"https://www.instagram.com/{quote(username)}/?__a=1"
    try:
        async with session.get(url, headers=HEADERS) as resp:
            if resp.status == 200:
                data = await resp.json()
                user = data.get("graphql", {}).get("user", {})
                return {
                    "username": user.get("username"),
                    "full_name": user.get("full_name"),
                    "bio": user.get("biography"),
                    "followers": user.get("edge_followed_by", {}).get("count"),
                    "following": user.get("edge_follow", {}).get("count"),
                    "posts": user.get("edge_owner_to_timeline_media", {}).get("count"),
                    "is_private": user.get("is_private"),
                    "profile_pic": user.get("profile_pic_url_hd") or user.get("profile_pic_url"),
                }
            return {}
    except Exception as e:
        logger.error(f"Ошибка при скрапинге Instagram: {e}")
        return {}


# =================== ОСНОВНАЯ ФУНКЦИЯ МОДУЛЯ ===================

async def gather(target: str, use_proxy: bool = False) -> Dict[str, any]:
    """
    Основная функция модуля: собирает данные из соцсетей.
    Автоматически определяет тип цели (email, имя, username).
    """
    logger.info(f"Запуск модуля social для цели: {target}")

    results = {
        "target": target,
        "vk": [],
        "telegram": [],
        "twitter": [],
        "instagram": [],
        "ai": {}
    }

    # Определяем, что за цель
    if "@" in target and "." in target:
        # Это email — попробуем извлечь имя
        name_part = target.split("@")[0]
        search_name = re.sub(r"[._0-9]", " ", name_part).title()
    elif target.startswith("http"):
        extracted = extract_username_from_url(target)
        if extracted:
            target = extracted
        search_name = target
    else:
        search_name = target

    # Получаем сессию (с прокси/Tor при необходимости)
    session = await get_session("tor" if use_proxy else None)

    try:
        # === 1. Поиск в VK по имени ===
        if search_name and len(search_name) > 2:
            vk_users = await search_vk_by_name(session, search_name)
            results["vk"] = vk_users

            # Доп. данные по первому пользователю
            if vk_users:
                                profile = await get_vk_profile(session, vk_users[0]["id"])
                                results["vk_profile"] = profile

        # === 2. Поиск в Telegram ===
        if target.isalnum() or len(target) <= 30:  # Похоже на username
            tg_results = await search_telegram(session, target)
            results["telegram"] = tg_results

        # === 3. Поиск в Twitter ===
        if target.isalnum() or target.startswith("@"):
            username = target.lstrip("@")
            twitter_user = await search_twitter(session, username)
            results["twitter"] = twitter_user

        # Поиск по имени
        if search_name and not results["twitter"]:
            tw_by_name = await search_twitter_by_name(session, search_name)
            results["twitter_by_name"] = tw_by_name

        # === 4. Instagram ===
        if target.isalnum():
            insta = await scrape_instagram_profile(session, target)
            if insta:
                results["instagram"] = [insta]

        # === 5. ИИ-анализ найденного текста ===
        text_corpus = " ".join([
            results.get("vk_profile", {}).get("about", ""),
            results.get("vk_profile", {}).get("interests", ""),
            results.get("telegram", [{}])[0].get("description", ""),
            results.get("twitter", [{}])[0].get("description", ""),
            results.get("instagram", [{}])[0].get("bio", "")
        ])

        if text_corpus.strip():
            results["ai"] = {
                "entities": extract_entities(text_corpus),
                "sentiment": sentiment(text_corpus),
                "summary": text_corpus[:300] + "..." if len(text_corpus) > 300 else text_corpus
            }

        logger.info(f"Модуль social завершил работу для {target}")
    except Exception as e:
        logger.error(f"Ошибка в модуле social: {e}")
        results["error"] = str(e)
    finally:
        await session.close()

    return results