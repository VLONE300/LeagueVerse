import re
import aiohttp
from datetime import datetime
from aiohttp import ClientSession
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from nba.models import NBAGame, NBATeam
from parsers.fetcher import fetch
from parsers.utils import extract_team_name


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


async def get_nba_standings():
    async with aiohttp.ClientSession() as session:
        return await scrape_nba_standings(session)


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
            date_game_str = row.find('th', {'data-stat': 'date_game'}).get_text()
            visitor_team = row.find('td', {'data-stat': 'visitor_team_name'}).get_text()
            visitor_pts = row.find('td', {'data-stat': 'visitor_pts'}).get_text()
            home_team = row.find('td', {'data-stat': 'home_team_name'}).get_text()
            home_pts = row.find('td', {'data-stat': 'home_pts'}).get_text()
            box_score_cell = row.find('td', {'data-stat': 'box_score_text'})
            box_score_link = box_score_cell.find('a')['href'] if box_score_cell and box_score_cell.find('a') else None
            # status = 'Finished' if box_score_link else 'Waiting'
            if box_score_link:
                await scrape_box_score(session, box_score_link)
                status = 'Finished'

            date_game = datetime.strptime(date_game_str, '%a, %b %d, %Y').date()

            visitor_team = await sync_to_async(NBATeam.objects.get)(name=visitor_team)
            home_team = await sync_to_async(NBATeam.objects.get)(name=home_team)

            match_exists = await sync_to_async(
                NBAGame.objects.filter(
                    date=date_game.strftime('%Y-%m-%d'),
                    visitor_team=visitor_team,
                    home_team=home_team,
                    box_score_link=box_score_link
                ).exists)()
            if match_exists:
                continue

            await sync_to_async(NBAGame.objects.update_or_create)(
                date=date_game.strftime('%Y-%m-%d'),
                visitor_team=visitor_team,
                home_team=home_team,
                defaults={
                    'visitor_pts': visitor_pts,
                    'home_pts': home_pts,
                    'box_score_link': box_score_link,
                    'status': status
                }
            )


async def scrape_nba_box_score(session: ClientSession, box_score_link):
    full_url = f'https://www.basketball-reference.com{box_score_link}'
    response = await fetch(session, full_url)
    soup = BeautifulSoup(response, 'lxml')
    tables = soup.find_all('table', id=re.compile(r'box-[A-Z]{3}-game-basic'))
    for i in tables:
        caption = i.find('caption').text
        team_name = caption[:caption.index('Basic') - 1]
        stats = i.find('tfoot').find_all('tr')
        for stat in stats:
            field_goals = stat.find('td', {'data-stat': 'fg'}).get_text()
            field_goal_attempts = stat.find('td', {'data-stat': 'fga'}).get_text()
            field_goals_percentage = stat.find('td', {'data-stat': 'fg_pct'}).get_text()
            three_point_field_goals = stat.find('td', {'data-stat': 'fg3'}).get_text()
            three_point_field_goal_attempts = stat.find('td', {'data-stat': 'fg3a'}).get_text()
            three_point_field_goals_percentage = stat.find('td', {'data-stat': 'fg3_pct'}).get_text()
            free_throws = stat.find('td', {'data-stat': 'ft'}).get_text()
            free_throw_attempts = stat.find('td', {'data-stat': 'fta'}).get_text()
            free_throw_percentage = stat.find('td', {'data-stat': 'ft_pct'}).get_text()
            personal_fouls = stat.find('td', {'data-stat': 'pf'}).get_text()
            total_rebounds = stat.find('td', {'data-stat': 'trb'}).get_text()
            offensive_rebounds = stat.find('td', {'data-stat': 'orb'}).get_text()
            turnovers = stat.find('td', {'data-stat': 'tov'}).get_text()
            assists = stat.find('td', {'data-stat': 'ast'}).get_text()
            steals = stat.find('td', {'data-stat': 'stl'}).get_text()
            blocks = stat.find('td', {'data-stat': 'blk'}).get_text()

            print({'team_name': team_name,
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


async def get_nba_box_score():
    async with aiohttp.ClientSession() as session:
        await scrape_nba_box_score(session, '/boxscores/202406060BOS.html')


async def get_nba_matches(season=2024):
    async with aiohttp.ClientSession() as session:
        await update_nba_matches(session, season)
