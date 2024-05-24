import asyncio
import fake_useragent
import aiohttp
from datetime import datetime
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from asgiref.sync import sync_to_async
from nba.models import NBATeam, NBAGame


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


async def update_matches(session: ClientSession, season: int):
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
            status = 'Finished' if box_score_link else 'Waiting'

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


async def get_matches(season=2024):
    async with aiohttp.ClientSession() as session:
        await update_matches(session, season)
