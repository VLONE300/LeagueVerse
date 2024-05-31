import asyncio
import re

import aiohttp
import fake_useragent
from aiohttp import ClientSession
from bs4 import BeautifulSoup

user = fake_useragent.UserAgent().random
header = {'user-agent': user}


async def fetch(session: ClientSession, url: str, sleep: int = 5, retries: int = 3) -> str:
    for i in range(1, retries + 1):
        await asyncio.sleep(sleep * i)
        try:
            async with session.get(url, headers=header) as response:
                response.raise_for_status()
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"Error fetching {url}: {e}")
    return None


async def scrape_nhl_standings(session: ClientSession, sleep: int = 5, retries: int = 3):
    standings_url = 'https://www.hockey-reference.com/leagues/NHL_2024_standings.html'
    standings_data = await fetch(session, standings_url, sleep=sleep, retries=retries)
    if standings_data is None:
        return None
    soup = BeautifulSoup(standings_data, 'lxml')

    data = []

    for conference in ['EAS', 'WES']:
        conference_table = soup.find('table', id=f'standings_{conference}')
        for row in conference_table.find('tbody').find_all('tr', class_='full_table'):
            name = row.find('th', {'data-stat': 'team_name'}).get_text()
            team_name = re.sub(r'[\*\u200b\xa0].*$', '', name).strip()
            games_played = row.find('td', {'data-stat': 'games'}).get_text()
            wins = row.find('td', {'data-stat': 'wins'}).get_text()
            losses = row.find('td', {'data-stat': 'losses'}).get_text()
            num_of_overtime_losses = row.find('td', {'data-stat': 'losses_ot'}).get_text()
            total_points = row.find('td', {'data-stat': 'points'}).get_text()
            points_percentage = row.find('td', {'data-stat': 'points_pct'}).get_text()
            goals_for = row.find('td', {'data-stat': 'goals'}).get_text()
            goals_against = row.find('td', {'data-stat': 'opp_goals'}).get_text()
            wins_of_regulation = row.find('td', {'data-stat': 'reg_wins'}).get_text()

            data.append({
                'team_name': team_name,
                'games_played': games_played,
                'wins': wins,
                'losses': losses,
                'num_of_overtime_losses': num_of_overtime_losses,
                'total_points': total_points,
                'points_percentage': points_percentage,
                'goals_for': goals_for,
                'goals_against': goals_against,
                'wins_of_regulation': wins_of_regulation
            })

    return data


async def get_nhl_standings():
    async with aiohttp.ClientSession() as session:
        return await scrape_nhl_standings(session)
