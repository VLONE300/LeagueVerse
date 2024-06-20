from aiohttp import ClientSession
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup

from nhl.models import NHLTeam, NHLGame
from parsers.fetcher import fetch
from parsers.utils import date_str_to_date


async def update_nhl_matches(session: ClientSession):
    season_url = 'https://www.hockey-reference.com/leagues/NHL_2024_games.html'
    games_data = await fetch(session, season_url)
    if not games_data:
        return None

    soup = BeautifulSoup(games_data, 'lxml')

    for table in ('_playoffs', ''):
        games = soup.find('table', id=f'games{table}')
        for game in reversed(games.find('tbody').find_all('tr')):
            date_game = date_str_to_date(game.find('th', {'data-stat': 'date_game'}).text)
            visitor_team = game.find('td', {'data-stat': 'visitor_team_name'}).text
            visitor_pts = game.find('td', {'data-stat': 'visitor_goals'}).text
            visitor_pts = int(visitor_pts) if visitor_pts.isdigit() else None
            home_team = game.find('td', {'data-stat': 'home_team_name'}).text
            home_pts = game.find('td', {'data-stat': 'home_goals'}).text
            home_pts = int(home_pts) if home_pts.isdigit() else None
            overtime = game.find('td', {'data-stat': 'overtimes'}).text
            box_score_cell = game.find('th', {'data-stat': 'date_game'})
            box_score_link = box_score_cell.find('a')['href'] if box_score_cell.find('a') else None
            game_type = 'Regular Season' if table == '' else 'Playoff'
            status = 'Finished' if box_score_link else 'Waiting'

            visitor_team = await sync_to_async(NHLTeam.objects.get)(name=visitor_team)
            home_team = await sync_to_async(NHLTeam.objects.get)(name=home_team)

            match_exists = await sync_to_async(
                NHLGame.objects.filter(
                    date=date_game.strftime('%Y-%m-%d'),
                    visitor_team=visitor_team,
                    home_team=home_team,
                ).exists)()

            if match_exists:
                continue

            await sync_to_async(NHLGame.objects.update_or_create)(
                date=date_game.strftime('%Y-%m-%d'),
                visitor_team=visitor_team,
                home_team=home_team,
                defaults={
                    'visitor_pts': visitor_pts,
                    'home_pts': home_pts,
                    'status': status,
                    'overtime': overtime,
                    'type': game_type,
                }
            )
