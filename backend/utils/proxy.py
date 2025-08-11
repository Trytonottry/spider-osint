# utils/proxy.py
import aiohttp
from aiohttp_socks import ProxyConnector

async def get_session(proxy: str = None):
    if proxy and "tor" in proxy:
        connector = ProxyConnector.from_url("socks5://tor:9050")
        return aiohttp.ClientSession(connector=connector)
    return aiohttp.ClientSession()