from django.db.models import Sum
from nhl.models import NHLGame
from core.utils import get_games, calculate_stat


def team_gpg(teams):
    """Goals Per Game"""
    return calculate_stat(NHLGame, teams, 'visitor_pts', 'home_pts')


def team_ppg(teams):
    """Power Play Goals"""
    team_ppp_data = []
    for team in teams:
        visitor_games = get_games(NHLGame, team, is_home=False)
        home_games = get_games(NHLGame, team, is_home=True)

        if visitor_games:
            visitor_power_play_goals = visitor_games.aggregate(
                total=Sum('box_score__visitor_team_stats__power_play_goals'))['total']
        else:
            visitor_power_play_goals = 0
        if home_games:
            home_power_play_goals = home_games.aggregate(
                total=Sum('box_score__home_team_stats__power_play_goals'))['total']
        else:
            home_power_play_goals = 0
        total_power_play_goals = visitor_power_play_goals + home_power_play_goals

        team_ppp_data.append({
            'team': team.name,
            'value': total_power_play_goals
        })
    return sorted(team_ppp_data, key=lambda x: x['value'], reverse=True)[:5]


def team_pim(teams):
    """Penalties Minutes"""
    team_pim_data = []
    for team in teams:
        visitor_games = get_games(NHLGame, team, is_home=False)
        home_games = get_games(NHLGame, team, is_home=True)

        if visitor_games:
            visitor_penalties_in_minutes = visitor_games.aggregate(
                total=Sum('box_score__visitor_team_stats__penalties_in_minutes'))['total']
        else:
            visitor_penalties_in_minutes = 0
        if home_games:
            home_penalties_in_minutes = home_games.aggregate(
                total=Sum('box_score__home_team_stats__penalties_in_minutes'))['total']
        else:
            home_penalties_in_minutes = 0
        total_penalties_in_minutes = visitor_penalties_in_minutes + home_penalties_in_minutes

        team_pim_data.append({
            'team': team.name,
            'value': round(total_penalties_in_minutes, 1)
        })
    return sorted(team_pim_data, key=lambda x: x['value'], reverse=True)[:5]


def team_ast(teams):
    """Assists made"""
    return calculate_stat(NHLGame, teams, 'box_score__visitor_team_stats__assists',
                          'box_score__home_team_stats__assists')


def team_sog(teams):
    """Shots On Goal"""
    return calculate_stat(NHLGame, teams, 'box_score__visitor_team_stats__shots_on_goal',
                          'box_score__home_team_stats__shots_on_goal')


def team_shg(teams):
    """Short Handed Goals"""
    team_shg_data = []
    for team in teams:
        visitor_games = get_games(NHLGame, team, is_home=False)
        home_games = get_games(NHLGame, team, is_home=True)

        if visitor_games:
            visitor_short_handed_goals = visitor_games.aggregate(
                total=Sum('box_score__visitor_team_stats__short_handed_goals'))['total']
        else:
            visitor_short_handed_goals = 0
        if home_games:
            home_short_handed_goals = home_games.aggregate(
                total=Sum('box_score__home_team_stats__short_handed_goals'))['total']
        else:
            home_short_handed_goals = 0
        total_short_handed_goals = visitor_short_handed_goals + home_short_handed_goals

        team_shg_data.append({
            'team': team.name,
            'value': total_short_handed_goals
        })
    return sorted(team_shg_data, key=lambda x: x['value'], reverse=True)[:5]


def get_nhl_stats(teams):
    return {
        'Goals Per Game': team_gpg(teams),
        'Assists': team_ast(teams),
        'Shots': team_sog(teams),
        'Power Play Goals': team_ppg(teams),
        'Short Handed Goals': team_shg(teams),
        'Penalties Minutes': team_pim(teams),
    }
