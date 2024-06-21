import aiohttp
from parsers.nhl.games import update_nhl_matches
from parsers.nhl.standings import update_nhl_standings


async def get_nhl_standings():
    async with aiohttp.ClientSession() as session:
        return await update_nhl_standings(session)


async def get_nhl_matches():
    async with aiohttp.ClientSession() as session:
        await update_nhl_matches(session)
