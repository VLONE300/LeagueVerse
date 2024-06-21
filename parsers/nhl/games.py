import re

from aiohttp import ClientSession
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup

from nhl.models import NHLTeam, NHLGame, NHLBoxScore, NHLTeamStats
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
            time = game.find('th', {'data-stat': 'time_game'}).text
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

            box_score = None

            if box_score_link:
                stats = await scrape_nhl_box_score_link(session, box_score_link)
                visitor_team_stats, home_team_stats = await save_nhl_team_stats(stats)
                box_score = await save_nhl_box_score(visitor_team_stats, home_team_stats)

            visitor_team = await sync_to_async(NHLTeam.objects.get)(name=visitor_team)
            home_team = await sync_to_async(NHLTeam.objects.get)(name=home_team)

            if await is_game_exist(date_game, visitor_team, home_team):
                continue

            await save_nhl_game(date_game, visitor_team, home_team, visitor_pts, home_pts, box_score, status, time,
                                overtime, game_type)


async def is_game_exist(date_game, visitor_team, home_team):
    match_exists = await sync_to_async(
        NHLGame.objects.filter(
            date=date_game,
            visitor_team=visitor_team,
            home_team=home_team,
            status='Finished'
        ).exists)()
    return match_exists


async def save_nhl_game(date_game, visitor_team, home_team, visitor_pts, home_pts, box_score, status, time, overtime,
                        game_type):
    await sync_to_async(NHLGame.objects.update_or_create)(
        date=date_game.strftime('%Y-%m-%d'),
        visitor_team=visitor_team,
        home_team=home_team,
        defaults={
            'visitor_pts': visitor_pts,
            'home_pts': home_pts,
            'box_score': box_score,
            'status': status,
            'overtime': overtime,
            'time': time,
            'type': game_type,
        }
    )


async def save_nhl_box_score(visitor_team_stats, home_team_stats):
    box_score = await sync_to_async(NHLBoxScore.objects.create)(
        visitor_team_stats=visitor_team_stats,
        home_team_stats=home_team_stats
    )
    return box_score


async def save_nhl_team_stats(stats):
    visitor_team_stats = await sync_to_async(NHLTeamStats.objects.create)(**stats[0])
    home_team_stats = await sync_to_async(NHLTeamStats.objects.create)(**stats[1])
    return visitor_team_stats, home_team_stats


async def scrape_nhl_box_score_link(session, box_score_link):
    full_url = f'https://www.hockey-reference.com{box_score_link}'
    response = await fetch(session, full_url)
    soup = BeautifulSoup(response, 'lxml')
    tables = soup.find_all('table', id=re.compile(r'[A-Z]{3}_skaters'))
    nhl_stats = []
    for i in tables:
        team_totals = i.find('tfoot').find_all('tr')
        for totals in team_totals:
            goals = totals.find('td', {'data-stat': 'goals'}).text
            assists = totals.find('td', {'data-stat': 'ast'}).text
            points = totals.find('td', {'data-stat': 'points'}).text
            penalties_in_minutes = totals.find('td', {'data-stat': 'pen_min'}).text
            even_strength_goals = totals.find('td', {'data-stat': 'goals_ev'}).text
            power_play_goals = totals.find('td', {'data-stat': 'goals_pp'}).text
            short_handed_goals = totals.find('td', {'data-stat': 'goals_sh'}).text
            shots_on_goal = totals.find('td', {'data-stat': 'shots'}).text
            shooting_percentage = totals.find('td', {'data-stat': 'shot_pct'})
            nhl_stats.append({
                'goals': goals,
                'assists': assists,
                'points': points,
                'penalties_in_minutes': penalties_in_minutes,
                'even_strength_goals': even_strength_goals,
                'power_play_goals': power_play_goals,
                'short_handed_goals': short_handed_goals,
                'shots_on_goal': shots_on_goal,
                'shooting_percentage': shooting_percentage
            })
    return nhl_stats
