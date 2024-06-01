from asgiref.sync import async_to_sync
from celery import shared_task
from nhl.models import NHLStanding, NHLTeam
from parsers.nhl.utils import get_nhl_standings, get_nhl_matches


@shared_task
def parse_nhl_games():
    import asyncio
    asyncio.run(get_nhl_matches())

@shared_task
def save_nhl_standings():
    standings_data = async_to_sync(get_nhl_standings)()
    for data in standings_data:
        team = NHLTeam.objects.get(name=data['team_name'])
        NHLStanding.objects.update_or_create(
            team=team,
            defaults={
                'games_played': data['games_played'],
                'wins': data['wins'],
                'losses': data['losses'],
                'num_of_overtime_losses': data['num_of_overtime_losses'],
                'total_points': data['total_points'],
                'points_percentage': data['points_percentage'],
                'goals_for': data['goals_for'],
                'goals_against': data['goals_against'],
                'wins_of_regulation': data['wins_of_regulation'],
            }
        )
