import aiohttp
from parsers.nba.games import update_nba_matches
from parsers.nba.standings import update_nba_standings


async def get_nba_standings():
    async with aiohttp.ClientSession() as session:
        await update_nba_standings(session)


async def get_nba_matches(season=2024):
    async with aiohttp.ClientSession() as session:
        await update_nba_matches(session, season)
