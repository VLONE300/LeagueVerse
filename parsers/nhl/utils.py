import asyncio
import re
from datetime import datetime

import aiohttp
from aiohttp import ClientSession
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup

from nhl.models import NHLTeam, NHLGame
from parsers.fetcher import fetch
from parsers.utils import extract_team_name


async def scrape_nhl_standings(session: ClientSession, sleep: int = 5, retries: int = 3):
    nhl_standings_url = 'https://www.hockey-reference.com/leagues/NHL_2024_standings.html'
    standings_data = await fetch(session, nhl_standings_url, sleep=sleep, retries=retries)
    if standings_data is None:
        return None

    soup = BeautifulSoup(standings_data, 'lxml')
    data = []

    for conference in ['EAS', 'WES']:
        conference_table = soup.find('table', id=f'standings_{conference}')
        for row in conference_table.find('tbody').find_all('tr', class_='full_table'):
            team_name = extract_team_name(row)
            data.append({
                'team_name': team_name,
                'games_played': row.find('td', {'data-stat': 'games'}).get_text(),
                'wins': row.find('td', {'data-stat': 'wins'}).get_text(),
                'losses': row.find('td', {'data-stat': 'losses'}).get_text(),
                'num_of_overtime_losses': row.find('td', {'data-stat': 'losses_ot'}).get_text(),
                'total_points': row.find('td', {'data-stat': 'points'}).get_text(),
                'points_percentage': row.find('td', {'data-stat': 'points_pct'}).get_text(),
                'goals_for': row.find('td', {'data-stat': 'goals'}).get_text(),
                'goals_against': row.find('td', {'data-stat': 'opp_goals'}).get_text(),
                'wins_of_regulation': row.find('td', {'data-stat': 'reg_wins'}).get_text(),
            })

    return data


async def get_nhl_standings():
    async with aiohttp.ClientSession() as session:
        return await scrape_nhl_standings(session)


async def update_nhl_matches(session: ClientSession):
    season_url = 'https://www.hockey-reference.com/leagues/NHL_2024_games.html'
    games_data = await fetch(session, season_url)
    if not games_data:
        return None

    soup = BeautifulSoup(games_data, 'lxml')

    for table in ('_playoffs', ''):
        games = soup.find('table', id=f'games{table}')
        for game in reversed(games.find('tbody').find_all('tr')):
            date_game_str = game.find('th', {'data-stat': 'date_game'}).text
            visitor_team = game.find('td', {'data-stat': 'visitor_team_name'}).text
            visitor_pts = game.find('td', {'data-stat': 'visitor_goals'}).text
            home_team = game.find('td', {'data-stat': 'home_team_name'}).text
            home_pts = game.find('td', {'data-stat': 'home_goals'}).text
            overtime = game.find('td', {'data-stat': 'overtimes'}).text
            box_score_cell = game.find('th', {'data-stat': 'date_game'})
            box_score_link = box_score_cell.find('a')['href'] if box_score_cell.find('a') else None
            game_type = 'Regular Season' if table == '' else 'Playoff'
            status = 'Finished' if box_score_link else 'Waiting'

            date_game = datetime.strptime(date_game_str, '%Y-%m-%d').date()

            visitor_team = await sync_to_async(NHLTeam.objects.get)(name=visitor_team)
            home_team = await sync_to_async(NHLTeam.objects.get)(name=home_team)

            match_exists = await sync_to_async(
                NHLGame.objects.filter(
                    date=date_game.strftime('%Y-%m-%d'),
                    visitor_team=visitor_team,
                    home_team=home_team,
                    box_score_link=box_score_link
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
                    'box_score_link': box_score_link,
                    'status': status,
                    'overtime': overtime,
                    'type': game_type,
                }
            )
async def update_nhl_matches(session: ClientSession):
    season_url = 'https://www.hockey-reference.com/leagues/NHL_2024_games.html'
    games_data = await fetch(session, season_url)
    if not games_data:
        return None

    soup = BeautifulSoup(games_data, 'lxml')

    for table in ('_playoffs', ''):
        games = soup.find('table', id=f'games{table}')
        for game in reversed(games.find('tbody').find_all('tr')):
            date_game_str = game.find('th', {'data-stat': 'date_game'}).text
            visitor_team = game.find('td', {'data-stat': 'visitor_team_name'}).text
            visitor_pts = game.find('td', {'data-stat': 'visitor_goals'}).text
            home_team = game.find('td', {'data-stat': 'home_team_name'}).text
            home_pts = game.find('td', {'data-stat': 'home_goals'}).text
            overtime = game.find('td', {'data-stat': 'overtimes'}).text
            box_score_cell = game.find('th', {'data-stat': 'date_game'})
            box_score_link = box_score_cell.find('a')['href'] if box_score_cell.find('a') else None
            game_type = 'Regular Season' if table == '' else 'Playoff'
            status = 'Finished' if box_score_link else 'Waiting'

            date_game = datetime.strptime(date_game_str, '%Y-%m-%d').date()

            visitor_team = await sync_to_async(NHLTeam.objects.get)(name=visitor_team)
            home_team = await sync_to_async(NHLTeam.objects.get)(name=home_team)

            match_exists = await sync_to_async(
                NHLGame.objects.filter(
                    date=date_game.strftime('%Y-%m-%d'),
                    visitor_team=visitor_team,
                    home_team=home_team,
                    box_score_link=box_score_link
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
                    'box_score_link': box_score_link,
                    'status': status,
                    'overtime': overtime,
                    'type': game_type,
                }
            )




async def get_nhl_matches():
    async with aiohttp.ClientSession() as session:
        await update_nhl_matches(session)
