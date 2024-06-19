import asyncio
from celery import shared_task
from parsers.nba.utils import get_nba_standings, get_nba_matches


@shared_task
def parse_nba_games():
    import asyncio
    asyncio.run(get_nba_matches())


@shared_task
def save_nba_standings():
    asyncio.run(get_nba_standings())
