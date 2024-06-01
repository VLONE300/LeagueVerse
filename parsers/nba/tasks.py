from asgiref.sync import async_to_sync
from celery import shared_task

from nba.models import NBATeam, NBAStanding
from parsers.nba.utils import get_nba_standings, get_nba_matches

@shared_task
def parse_nba_games():
    import asyncio
    asyncio.run(get_nba_matches())


@shared_task
def save_nba_standings():
    standings_data = async_to_sync(get_nba_standings)()
    for data in standings_data:
        team = NBATeam.objects.get(name=data['team_name'])
        NBAStanding.objects.update_or_create(
            team=team,
            defaults={
                'wins': data['wins'],
                'losses': data['losses'],
                'winning_percentage': data['winrate'],
                'games_back': data['gb'],
                'points_percentage_game': data['points'],
                'oop_points_percentage_game': data['opp_points'],

            }
        )
