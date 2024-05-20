import re
import fake_useragent
import requests
from bs4 import BeautifulSoup

user = fake_useragent.UserAgent().random
header = {'user-agent': user}


def scrape_standings():
    link = 'https://www.basketball-reference.com/leagues/NBA_2024_standings.html'
    response = requests.get(link, headers=header).text
    soup = BeautifulSoup(response, 'lxml')

    data = []

    for conference in ['E', 'W']:
        conference_table = soup.find('table', id=f'confs_standings_{conference}')
        for row in conference_table.find('tbody').find_all('tr', class_='full_table'):
            name = row.find('th', {'data-stat': 'team_name'}).get_text()
            team_name = re.sub(r'[\*\u200b\xa0].*$', '', name).strip()
            wins = row.find('td', {'data-stat': 'wins'}).get_text()
            losses = row.find('td', {'data-stat': 'losses'}).get_text()
            winrate = row.find('td', {'data-stat': 'win_loss_pct'}).get_text()
            games_back = row.find('td', {'data-stat': 'gb'}).get_text()
            points = row.find('td', {'data-stat': 'pts_per_g'}).get_text()
            opp_points = row.find('td', {'data-stat': 'opp_pts_per_g'}).get_text()

            data.append({
                'team_name': team_name,
                'wins': wins,
                'losses': losses,
                'winrate': winrate,
                'gb': games_back,
                'points': points,
                'opp_points': opp_points
            })

    return data
