from celery import shared_task

from nba.models import NBATeam, NBAStanding
from .fetcher import get_matches
from .utils import scrape_standings


@shared_task
def parse_nba_games():
    import asyncio
    asyncio.run(get_matches())

@shared_task
def save_nba_standings():
    for data in scrape_standings():
        standings_instance, created = NBAStanding.objects.update_or_create(
            team_id=NBATeam.objects.get(name=data['team_name']).id,
            defaults={
                'wins': data['wins'],
                'losses': data['losses'],
                'winning_percentage': data['winrate'],
                'games_back': data['gb'],
                'points_percentage_game': data['points'],
                'oop_points_percentage_game': data['opp_points'],

            }
        )
