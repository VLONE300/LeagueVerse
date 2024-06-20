from aiohttp import ClientSession
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup

from nba.models import NBATeam, NBAStanding
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


async def update_nba_standings(session: ClientSession):
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
