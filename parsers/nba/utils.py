import aiohttp
from parsers.nba.games import update_nba_matches
from parsers.nba.standings import update_nba_standings


async def get_nba_standings():
    async with aiohttp.ClientSession() as session:
        await update_nba_standings(session, 2024)


async def get_nba_matches():
    async with aiohttp.ClientSession() as session:
        await update_nba_matches(session, 2024)
