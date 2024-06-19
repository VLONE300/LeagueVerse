import re


def extract_team_name(row):
    """Delete extra characters"""
    name = row.find('th', {'data-stat': 'team_name'}).get_text()
    return re.sub(r'[\*\u200b\xa0].*$', '', name).strip()
