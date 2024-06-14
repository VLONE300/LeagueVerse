import re
import aiohttp
from datetime import datetime
from aiohttp import ClientSession
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from nba.models import NBAGame, NBATeam, NBATeamStats, NBABoxScore
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


@sync_to_async
def get_nba_team(name):
    return NBATeam.objects.get(name=name)


@sync_to_async
def create_or_update_nba_game(date, visitor_team, home_team, visitor_pts, home_pts, status):
    return NBAGame.objects.update_or_create(
        date=date,
        visitor_team=visitor_team,
        home_team=home_team,
        defaults={
            'visitor_pts': visitor_pts,
            'home_pts': home_pts,
            'status': status
        }
    )


async def update_nba_matches(session, season):
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
            visitor_team_name = row.find('td', {'data-stat': 'visitor_team_name'}).get_text()
            visitor_pts = int(row.find('td', {'data-stat': 'visitor_pts'}).get_text())
            home_team_name = row.find('td', {'data-stat': 'home_team_name'}).get_text()
            home_pts = int(row.find('td', {'data-stat': 'home_pts'}).get_text())
            box_score_cell = row.find('td', {'data-stat': 'box_score_text'})
            box_score_link = box_score_cell.find('a')['href'] if box_score_cell and box_score_cell.find('a') else None
            status = 'Finished' if box_score_link else 'Waiting'

            date_game = datetime.strptime(date_game_str, '%a, %b %d, %Y').date()

            visitor_team = await get_nba_team(visitor_team_name)
            home_team = await get_nba_team(home_team_name)

            match_exists = await sync_to_async(
                NBAGame.objects.filter(
                    date=date_game,
                    visitor_team=visitor_team,
                    home_team=home_team,
                ).exists)()
            if match_exists:
                continue

            await create_or_update_nba_game(
                date=date_game,
                visitor_team=visitor_team,
                home_team=home_team,
                visitor_pts=visitor_pts,
                home_pts=home_pts,
                status=status
            )

            game = await sync_to_async(NBAGame.objects.get)(
                date=date_game,
                visitor_team=visitor_team,
                home_team=home_team,
            )
            print(game)


async def scrape_and_save_box_score(session, nba_game, box_score_link):
    full_url = f'https://www.basketball-reference.com{box_score_link}'
    response = await fetch(session, full_url)
    soup = BeautifulSoup(response, 'lxml')
    tables = soup.find_all('table', id=re.compile(r'box-[A-Z]{3}-game-basic'))
    for table in tables:
        caption = table.find('caption').text
        team_name = caption.split(' ')[0]  # первое слово в заголовке является именем команды

        # Используем sync_to_async для создания/получения объекта NBATeamStats
        team_stats, _ = await sync_to_async(NBATeamStats.objects.get_or_create)(
            team=await sync_to_async(NBATeam.objects.get_or_create)(name=team_name)[0]
        )

        # Парсинг статистики для каждой команды
        team_stats.field_goals = int(table.find('tfoot').find('td', {'data-stat': 'fg'}).get_text())
        team_stats.field_goal_attempts = int(table.find('tfoot').find('td', {'data-stat': 'fga'}).get_text())
        team_stats.field_goals_percentage = float(table.find('tfoot').find('td', {'data-stat': 'fg_pct'}).get_text())
        team_stats.three_point_field_goals = int(table.find('tfoot').find('td', {'data-stat': 'fg3'}).get_text())
        team_stats.three_point_field_goal_attempts = int(
            table.find('tfoot').find('td', {'data-stat': 'fg3a'}).get_text())
        team_stats.three_point_field_goals_percentage = float(
            table.find('tfoot').find('td', {'data-stat': 'fg3_pct'}).get_text())
        team_stats.free_throws = int(table.find('tfoot').find('td', {'data-stat': 'ft'}).get_text())
        team_stats.free_throw_attempts = int(table.find('tfoot').find('td', {'data-stat': 'fta'}).get_text())
        team_stats.free_throw_percentage = float(table.find('tfoot').find('td', {'data-stat': 'ft_pct'}).get_text())
        team_stats.personal_fouls = int(table.find('tfoot').find('td', {'data-stat': 'pf'}).get_text())
        team_stats.total_rebounds = int(table.find('tfoot').find('td', {'data-stat': 'trb'}).get_text())
        team_stats.offensive_rebounds = int(table.find('tfoot').find('td', {'data-stat': 'orb'}).get_text())
        team_stats.turnovers = int(table.find('tfoot').find('td', {'data-stat': 'tov'}).get_text())
        team_stats.assists = int(table.find('tfoot').find('td', {'data-stat': 'ast'}).get_text())
        team_stats.steals = int(table.find('tfoot').find('td', {'data-stat': 'stl'}).get_text())
        team_stats.blocks = int(table.find('tfoot').find('td', {'data-stat': 'blk'}).get_text())

        await sync_to_async(team_stats.save)()

        # Создаем объект NBABoxScore для текущего NBAGame
        await sync_to_async(NBABoxScore.objects.create)(
            game=nba_game,
            home_team_stats=team_stats if nba_game.home_team == team_stats.team else None,
            visitor_team_stats=team_stats if nba_game.visitor_team == team_stats.team else None,
        )


async def get_nba_matches(season=2024):
    async with aiohttp.ClientSession() as session:
        await update_nba_matches(session, season)
