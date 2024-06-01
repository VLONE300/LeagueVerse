import asyncio
import aiohttp
import fake_useragent
from aiohttp import ClientSession

user = fake_useragent.UserAgent().random
header = {'user-agent': user}


async def fetch(session: ClientSession, url: str, sleep: int = 5, retries: int = 3):
    for i in range(1, retries + 1):
        await asyncio.sleep(sleep * i)
        try:
            async with session.get(url, headers=header) as response:
                response.raise_for_status()
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"Error fetching {url}: {e}")
    return None
