import re
import aiohttp
from datetime import datetime
from aiohttp import ClientSession
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from nba.models import NBAGame, NBATeam, NBABoxScore, NBATeamStats, NBAStanding
from parsers.fetcher import fetch
from parsers.utils import extract_team_name, date_str_to_date


async def scrape_nba_standings(session: ClientSession, sleep: int = 5, retries: int = 3):
    nba_standings_url = 'https://www.basketball-reference.com/leagues/NBA_2024_standings.html'
    standings_data = await fetch(session, nba_standings_url, sleep=sleep, retries=retries)
    if standings_data is None:
        return None

    soup = BeautifulSoup(standings_data, 'lxml')
    data = []

    for conference in ['E', 'W']:
        conference_table = soup.find('table', id=f'confs_standings_{conference}')
        for row in conference_table.find('tbody').find_all('tr', class_='full_table'):
            team_name = extract_team_name(row)
            data.append({
                'team_name': team_name,
                'wins': row.find('td', {'data-stat': 'wins'}).get_text(),
                'losses': row.find('td', {'data-stat': 'losses'}).get_text(),
                'winrate': row.find('td', {'data-stat': 'win_loss_pct'}).get_text(),
                'gb': row.find('td', {'data-stat': 'gb'}).get_text(),
                'points': row.find('td', {'data-stat': 'pts_per_g'}).get_text(),
                'opp_points': row.find('td', {'data-stat': 'opp_pts_per_g'}).get_text(),
            })
    return data


async def update_nba_standings(session: aiohttp.ClientSession):
    standings_data = await scrape_nba_standings(session)
    if standings_data is None:
        return

    for data in standings_data:
        team = await sync_to_async(NBATeam.objects.get)(name=data['team_name'])
        await sync_to_async(NBAStanding.objects.update_or_create)(
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


async def get_nba_standings():
    async with aiohttp.ClientSession() as session:
        await update_nba_standings(session)


async def scrape_season(session: ClientSession, season: int) -> list:
    season_url = f'https://www.basketball-reference.com/leagues/NBA_{season}_games.html'
    response = await fetch(session, season_url)

    if response is None:
        return []

    soup = BeautifulSoup(response, 'lxml')
    block = soup.find('div', class_='filter')
    links = block.find_all('a')
    href = [link['href'] for link in links]
    standings_pages = [f'https://www.basketball-reference.com{link}' for link in href]

    return standings_pages[::-1]


async def update_nba_matches(session: ClientSession, season: int):
    standings_pages = await scrape_season(session, season)
    if not standings_pages:
        return

    for month in standings_pages:
        response = await fetch(session, month)
        if response is None:
            continue

        soup = BeautifulSoup(response, 'lxml')
        table = soup.find('table', id='schedule')
        if not table:
            continue

        for row in reversed(table.find('tbody').find_all('tr')):
            date_game = date_str_to_date(row.find('th', {'data-stat': 'date_game'}).get_text())
            time = row.find('td', {'data-stat': 'game_start_time'}).get_text()
            visitor_team = row.find('td', {'data-stat': 'visitor_team_name'}).get_text()
            visitor_pts = row.find('td', {'data-stat': 'visitor_pts'}).get_text()
            visitor_pts = int(visitor_pts) if visitor_pts.isdigit() else None
            home_team = row.find('td', {'data-stat': 'home_team_name'}).get_text()
            home_pts = row.find('td', {'data-stat': 'home_pts'}).get_text()
            home_pts = int(home_pts) if home_pts.isdigit() else None
            box_score_cell = row.find('td', {'data-stat': 'box_score_text'})
            box_score_link = box_score_cell.find('a')['href'] if box_score_cell and box_score_cell.find('a') else None
            arena = row.find('td', {'data-stat': 'arena_name'}).get_text()
            status = 'Finished' if box_score_link else 'Waiting'

            box_score = None

            if box_score_link:
                stats = await scrape_nba_box_score_link(session, box_score_link)
                visitor_team_stats, home_team_stats = await save_nba_team_stats(stats)
                box_score = await save_nba_box_score(visitor_team_stats, home_team_stats)

            visitor_team = await sync_to_async(NBATeam.objects.get)(name=visitor_team)
            home_team = await sync_to_async(NBATeam.objects.get)(name=home_team)

            match_exists = await sync_to_async(
                NBAGame.objects.filter(
                    date=date_game,
                    visitor_team=visitor_team,
                    home_team=home_team,
                    status='Finished'
                ).exists)()
            if match_exists:
                continue

            print(date_game, visitor_team, visitor_pts, home_team, home_pts, box_score)
            await sync_to_async(NBAGame.objects.update_or_create)(
                date=date_game.strftime('%Y-%m-%d'),
                visitor_team=visitor_team,
                home_team=home_team,
                defaults={
                    'visitor_pts': visitor_pts,
                    'home_pts': home_pts,
                    'box_score': box_score,
                    'status': status,
                    'time': time,
                    'arena': arena
                }
            )


async def save_nba_box_score(visitor_team_stats, home_team_stats):
    box_score = await sync_to_async(NBABoxScore.objects.create)(
        visitor_team_stats=visitor_team_stats,
        home_team_stats=home_team_stats
    )
    return box_score


async def save_nba_team_stats(stats):
    visitor_team_stats = await sync_to_async(NBATeamStats.objects.create)(**stats[0])
    home_team_stats = await sync_to_async(NBATeamStats.objects.create)(**stats[1])
    return visitor_team_stats, home_team_stats


async def scrape_nba_box_score_link(session: ClientSession, box_score_link: str):
    full_url = f'https://www.basketball-reference.com{box_score_link}'
    response = await fetch(session, full_url)
    soup = BeautifulSoup(response, 'lxml')
    tables = soup.find_all('table', id=re.compile(r'box-[A-Z]{3}-game-basic'))
    stats = []
    for i in tables:
        team_totals = i.find('tfoot').find_all('tr')
        for totals in team_totals:
            field_goals = totals.find('td', {'data-stat': 'fg'}).get_text()
            field_goal_attempts = totals.find('td', {'data-stat': 'fga'}).get_text()
            field_goals_percentage = totals.find('td', {'data-stat': 'fg_pct'}).get_text()
            three_point_field_goals = totals.find('td', {'data-stat': 'fg3'}).get_text()
            three_point_field_goal_attempts = totals.find('td', {'data-stat': 'fg3a'}).get_text()
            three_point_field_goals_percentage = totals.find('td', {'data-stat': 'fg3_pct'}).get_text()
            free_throws = totals.find('td', {'data-stat': 'ft'}).get_text()
            free_throw_attempts = totals.find('td', {'data-stat': 'fta'}).get_text()
            free_throw_percentage = totals.find('td', {'data-stat': 'ft_pct'}).get_text()
            free_throw_percentage = None if free_throw_percentage == '' else float(free_throw_percentage)
            personal_fouls = totals.find('td', {'data-stat': 'pf'}).get_text()
            total_rebounds = totals.find('td', {'data-stat': 'trb'}).get_text()
            offensive_rebounds = totals.find('td', {'data-stat': 'orb'}).get_text()
            turnovers = totals.find('td', {'data-stat': 'tov'}).get_text()
            assists = totals.find('td', {'data-stat': 'ast'}).get_text()
            steals = totals.find('td', {'data-stat': 'stl'}).get_text()
            blocks = totals.find('td', {'data-stat': 'blk'}).get_text()
            stats.append({
                'field_goals': field_goals,
                'field_goal_attempts': field_goal_attempts,
                'field_goals_percentage': field_goals_percentage,
                'three_point_field_goals': three_point_field_goals,
                'three_point_field_goal_attempts': three_point_field_goal_attempts,
                'three_point_field_goals_percentage': three_point_field_goals_percentage,
                'free_throws': free_throws,
                'free_throw_attempts': free_throw_attempts,
                'free_throw_percentage': free_throw_percentage,
                'personal_fouls': personal_fouls,
                'total_rebounds': total_rebounds,
                'offensive_rebounds': offensive_rebounds,
                'turnovers': turnovers,
                'assists': assists,
                'steals': steals,
                'blocks': blocks
            })
    return stats


async def get_nba_matches(season=2024):
    async with aiohttp.ClientSession() as session:
        await update_nba_matches(session, season)
