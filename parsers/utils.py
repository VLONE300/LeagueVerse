import re
from datetime import datetime


def extract_team_name(row):
    """Delete extra characters"""
    name = row.find('th', {'data-stat': 'team_name'}).get_text()
    return re.sub(r'[\*\u200b\xa0].*$', '', name).strip()


def date_str_to_date(date_str):
    """Convert date string to datetime object"""
    date_game = datetime.strptime(date_str, '%a, %b %d, %Y').date()
    return date_game
