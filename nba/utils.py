from django.db.models import Sum
from nba.models import NBAGame
from core.utils import get_games, calculate_stat


def team_ppg(teams):
    """Points per game"""
    return calculate_stat(NBAGame, teams, 'visitor_pts', 'home_pts')


def team_apg(teams):
    """Assists Per Game"""
    return calculate_stat(NBAGame, teams, 'box_score__visitor_team_stats__assists',
                          'box_score__home_team_stats__assists')


def team_rpg(teams):
    """Rebounds Per Game"""
    return calculate_stat(NBAGame, teams, 'box_score__visitor_team_stats__total_rebounds',
                          'box_score__home_team_stats__total_rebounds')


def team_bpg(teams):
    """Blocks Per Game"""
    return calculate_stat(NBAGame, teams, 'box_score__visitor_team_stats__blocks',
                          'box_score__home_team_stats__blocks')


def team_spg(teams):
    """Steals Per Game"""
    return calculate_stat(NBAGame, teams, 'box_score__visitor_team_stats__steals',
                          'box_score__home_team_stats__steals')


def team_fgp(teams):
    """Field goals percentage"""
    return calculate_stat(NBAGame, teams, 'box_score__visitor_team_stats__field_goals_percentage',
                          'box_score__home_team_stats__field_goals_percentage', 100)


def team_3fg(teams):
    """Three pointers made"""
    team_3fg_data = []
    for team in teams:
        visitor_games = get_games(NBAGame, team, is_home=False)
        home_games = get_games(NBAGame, team, is_home=True)
        if visitor_games:
            visitor_three_pointers = visitor_games.aggregate(
                total=Sum('box_score__visitor_team_stats__three_point_field_goals'))['total']
        else:
            visitor_three_pointers = 0
        if home_games:
            home_three_pointers = home_games.aggregate(
                total=Sum('box_score__home_team_stats__three_point_field_goals'))['total']
        else:
            home_three_pointers = 0
        total_three_pointers = visitor_three_pointers + home_three_pointers

        team_3fg_data.append({
            'team': team.name,
            'value': round(total_three_pointers, 1)
        })
    return sorted(team_3fg_data, key=lambda x: x['value'], reverse=True)[:5]


def team_3fgp(teams):
    """Three point percentage"""
    return calculate_stat(NBAGame, teams, 'box_score__visitor_team_stats__three_point_field_goals_percentage',
                          'box_score__home_team_stats__three_point_field_goals_percentage', 100)


def team_ftp(teams):
    """Free throw percentage"""
    return calculate_stat(NBAGame, teams, 'box_score__visitor_team_stats__free_throw_percentage',
                          'box_score__home_team_stats__free_throw_percentage', 100)


def get_nba_stats(teams):
    return {
        'Points Per Game': team_ppg(teams),
        'Assists Per Game': team_apg(teams),
        'Rebounds Per Game': team_rpg(teams),
        'Blocks Per Game': team_bpg(teams),
        'Steals Per Game': team_spg(teams),
        'Field Goal Percentage': team_fgp(teams),
        'Three Pointers Made': team_3fg(teams),
        'Three Point Percentage': team_3fgp(teams),
        'Free Throw Percentage': team_ftp(teams)
    }
