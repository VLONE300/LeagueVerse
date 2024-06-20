from aiohttp import ClientSession
from bs4 import BeautifulSoup

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
