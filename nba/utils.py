from nba.models import NBAGame
from core.utils import calculate_top_5_avg_stat, calculate_top_5_sum_stat


def get_nba_stats(teams):
    stats = {
        'Points Per Game': calculate_top_5_avg_stat(
            NBAGame,
            teams,
            'visitor_pts',
            'home_pts'),
        'Assists Per Game': calculate_top_5_avg_stat(
            NBAGame,
            teams,
            'box_score__visitor_team_stats__assists',
            'box_score__home_team_stats__assists'),
        'Rebounds Per Game': calculate_top_5_avg_stat(
            NBAGame,
            teams,
            'box_score__visitor_team_stats__total_rebounds',
            'box_score__home_team_stats__total_rebounds'),
        'Blocks Per Game': calculate_top_5_avg_stat(
            NBAGame,
            teams,
            'box_score__visitor_team_stats__blocks',
            'box_score__home_team_stats__blocks'),
        'Steals Per Game': calculate_top_5_avg_stat(
            NBAGame,
            teams,
            'box_score__visitor_team_stats__steals',
            'box_score__home_team_stats__steals'),
        'Field Goal Percentage': calculate_top_5_avg_stat(
            NBAGame,
            teams,
            'box_score__visitor_team_stats__field_goals_percentage',
            'box_score__home_team_stats__field_goals_percentage',
            1),
        'Three Pointers Made': calculate_top_5_sum_stat(
            NBAGame,
            teams,
            'box_score__visitor_team_stats__three_point_field_goals',
            'box_score__home_team_stats__three_point_field_goals'),
        'Three Point Percentage': calculate_top_5_avg_stat(
            NBAGame,
            teams,
            'box_score__visitor_team_stats__three_point_field_goals_percentage',
            'box_score__home_team_stats__three_point_field_goals_percentage',
            1),
        'Free Throw Percentage': calculate_top_5_avg_stat(
            NBAGame,
            teams,
            'box_score__visitor_team_stats__free_throw_percentage',
            'box_score__home_team_stats__free_throw_percentage',
            1)
    }
    return stats


def get_nba_box_score(obj):
    return [
        {'name': 'Field Goals',
         'visitor_value': [obj.visitor_team_stats.field_goals, obj.visitor_team_stats.field_goal_attempts,
                           round(obj.visitor_team_stats.field_goals_percentage, 1)],
         'home_value': [obj.home_team_stats.field_goals, obj.home_team_stats.field_goal_attempts,
                        round(obj.home_team_stats.field_goals_percentage, 1)]},
        {'name': '3-Point FGs',
         'visitor_value': [obj.visitor_team_stats.three_point_field_goals,
                           obj.visitor_team_stats.three_point_field_goal_attempts,
                           round(obj.visitor_team_stats.three_point_field_goals_percentage, 1)],
         'home_value': [obj.home_team_stats.three_point_field_goals,
                        obj.home_team_stats.three_point_field_goal_attempts,
                        round(obj.home_team_stats.three_point_field_goals_percentage, 1)]},
        {'name': 'Free Throws',
         'visitor_value': [obj.visitor_team_stats.free_throws, obj.visitor_team_stats.free_throw_attempts,
                           round(obj.visitor_team_stats.free_throw_percentage, 1)],
         'home_value': [obj.home_team_stats.free_throws, obj.home_team_stats.free_throw_attempts,
                        round(obj.home_team_stats.free_throw_percentage, 1)]},

        {'name': 'Personal Fouls', 'visitor_value': obj.visitor_team_stats.personal_fouls,
         'home_value': obj.home_team_stats.personal_fouls},
        {'name': 'Total Rebounds', 'visitor_value': obj.visitor_team_stats.total_rebounds,
         'home_value': obj.home_team_stats.total_rebounds},
        {'name': 'Offensive Rebounds', 'visitor_value': obj.visitor_team_stats.offensive_rebounds,
         'home_value': obj.home_team_stats.offensive_rebounds},
        {'name': 'Turnovers', 'visitor_value': obj.visitor_team_stats.turnovers,
         'home_value': obj.home_team_stats.turnovers},
        {'name': 'Assists', 'visitor_value': obj.visitor_team_stats.assists,
         'home_value': obj.home_team_stats.assists},
        {'name': 'Blocks', 'visitor_value': obj.visitor_team_stats.blocks,
         'home_value': obj.home_team_stats.blocks},
        {'name': 'Steals', 'visitor_value': obj.visitor_team_stats.steals,
         'home_value': obj.home_team_stats.steals},
    ]
