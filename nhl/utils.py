from nhl.models import NHLGame
from core.utils import calculate_top_5_sum_stat, calculate_top_5_avg_stat


def get_nhl_stats(teams):
    stats = {
        'Goals Per Game': calculate_top_5_avg_stat(NHLGame, teams, 'visitor_pts', 'home_pts', 2),

        'Assists': calculate_top_5_avg_stat(NHLGame, teams, 'box_score__visitor_team_stats__assists',
                                            'box_score__home_team_stats__assists',2),

        'Shots': calculate_top_5_avg_stat(NHLGame, teams, 'box_score__visitor_team_stats__shots_on_goal',
                                          'box_score__home_team_stats__shots_on_goal'),

        'Power Play Goals': calculate_top_5_sum_stat(NHLGame, teams, 'box_score__visitor_team_stats__power_play_goals',
                                                     'box_score__home_team_stats__power_play_goals'),

        'Short Handed Goals': calculate_top_5_sum_stat(NHLGame, teams,
                                                       'box_score__visitor_team_stats__short_handed_goals',
                                                       'box_score__home_team_stats__short_handed_goals'),

        'Penalties Minutes': calculate_top_5_sum_stat(NHLGame, teams,
                                                      'box_score__visitor_team_stats__penalties_in_minutes',
                                                      'box_score__home_team_stats__penalties_in_minutes')
    }
    return stats


def get_nhl_box_score(obj):
    return [
        {'name': 'Goals', 'visitor_value': obj.visitor_team_stats.goals,
         'home_value': obj.home_team_stats.goals},
        {'name': 'Assists', 'visitor_value': obj.visitor_team_stats.assists,
         'home_value': obj.home_team_stats.assists},
        {'name': 'Points', 'visitor_value': obj.visitor_team_stats.points,
         'home_value': obj.home_team_stats.points},
        {'name': 'Penalties in minutes', 'visitor_value': obj.visitor_team_stats.penalties_in_minutes,
         'home_value': obj.home_team_stats.penalties_in_minutes},
        {'name': 'Power Play Goals', 'visitor_value': obj.visitor_team_stats.power_play_goals,
         'home_value': obj.home_team_stats.power_play_goals},
        {'name': 'Short Handed Goals', 'visitor_value': obj.visitor_team_stats.short_handed_goals,
         'home_value': obj.home_team_stats.short_handed_goals},
        {'name': 'Even Strength Goals', 'visitor_value': obj.visitor_team_stats.even_strength_goals,
         'home_value': obj.home_team_stats.even_strength_goals},
        {'name': 'Shots On Goal', 'visitor_value': obj.visitor_team_stats.shots_on_goal,
         'home_value': obj.home_team_stats.shots_on_goal},
        {'name': 'Shooting Percentage', 'visitor_value': obj.visitor_team_stats.shooting_percentage,
         'home_value': obj.home_team_stats.shooting_percentage},
    ]
