from celery import shared_task

from leagues.models import NBAStandings, NBATeams
from parsers.utils import parsing_nba_standings


@shared_task
def save_nba_standings():
    for data in parsing_nba_standings():
        if data['team_name'] == 'Nets':
            team = NBATeams.objects.get(name='Brooklyn Nets').id
        else:
            team = NBATeams.objects.get(name__icontains=data['team_name']).id
        standings_instance, created = NBAStandings.objects.update_or_create(
            team_id=team,
            defaults={
                'wins': data['wins'],
                'losses': data['losses'],
                'winning_percentage': data['winrate'],
                'games_back': data['gb'],
                'points_percentage_game': data['points'],
                'oop_points_percentage_game': data['opp_points'],
                'home_record': data['home'],
                'away_record': data['away'],
                'conference_record': data['conf'],
                'division_record': data['div'],
                'last_ten_games': data['L10'],
                'streak': data['streak']
            }
        )
