import aiohttp
from parsers.nhl.games import update_nhl_matches
from parsers.nhl.standings import scrape_nhl_standings


async def get_nhl_standings():
    async with aiohttp.ClientSession() as session:
        return await scrape_nhl_standings(session)


async def get_nhl_matches():
    async with aiohttp.ClientSession() as session:
        await update_nhl_matches(session)
