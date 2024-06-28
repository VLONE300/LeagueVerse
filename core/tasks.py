import asyncio
from celery import shared_task
from parsers.nhl.utils import get_nhl_matches, get_nhl_standings
from parsers.nba.utils import get_nba_standings, get_nba_matches


@shared_task
def parse_nba_games():
    asyncio.run(get_nba_matches())


@shared_task
def save_nba_standings():
    asyncio.run(get_nba_standings())


@shared_task
def parse_nhl_games():
    import asyncio
    asyncio.run(get_nhl_matches())


@shared_task
def save_nhl_standings():
    asyncio.run(get_nhl_standings())
