import requests
from bs4 import BeautifulSoup


def parsing_nba_standings():
    link = 'https://www.foxsports.com/nba/standings'
    response = requests.get(link).text
    soup = BeautifulSoup(response, 'lxml')

    data = []

    for conference in ['0', '1']:
        conference_table = soup.find('table', id=f'live-standings-table-{conference}')
        rows = conference_table.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 13:
                team_name = cells[1].find_all('a')[1].text.strip()
                wins = cells[2].find('div').text.strip()[:2]
                losses = cells[2].find('div').text.strip()[3:]
                winrate = cells[3].find('div').text.strip()
                gb = cells[4].find('div').text.strip()
                points = cells[5].find('div').text.strip()
                opp_points = cells[6].find('div').text.strip()
                home = cells[7].find('div').text.strip()
                away = cells[8].find('div').text.strip()
                conf = cells[9].find('div').text.strip()
                div = cells[10].find('div').text.strip()
                L10 = cells[11].find('div').text.strip()
                streak = cells[12].find('div').text.strip()

                data.append({
                    'team_name': team_name,
                    'wins': wins,
                    'losses': losses,
                    'winrate': winrate,
                    'gb': gb,
                    'points': points,
                    'opp_points': opp_points,
                    'home': home,
                    'away': away,
                    'conf': conf,
                    'div': div,
                    'L10': L10,
                    'streak': streak
                })
    return data
