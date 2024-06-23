from django.db.models import Avg, Sum
from nba.models import NBAGame


def get_games(team, is_home):
    """Get regular season home and away games"""
    field_name = 'home_team' if is_home else 'visitor_team'
    return NBAGame.objects.filter(**{field_name: team, 'type': 'Regular Season'})


def calculate_stat(teams, visitor_stat, home_stat, data_key, multiplier=1):
    """Calculate the average NBA statistic and return the top 5 teams by value"""
    stat_data = []
    for team in teams:
        visitor_games = get_games(team, is_home=False)
        home_games = get_games(team, is_home=True)

        visitor_value = visitor_games.aggregate(avg_value=Avg(visitor_stat))['avg_value']
        home_value = home_games.aggregate(avg_value=Avg(home_stat))['avg_value']

        avg_stat = ((visitor_value + home_value) / 2) * multiplier

        stat_data.append({
            'team': team.name,
            data_key: round(avg_stat, 1)
        })
    return sorted(stat_data, key=lambda x: x[data_key], reverse=True)[:5]


def team_ppg(teams):
    """Points per game"""
    return calculate_stat(teams, 'visitor_pts', 'home_pts', 'ppg')


def team_apg(teams):
    """Assists Per Game"""
    return calculate_stat(teams, 'box_score__visitor_team_stats__assists', 'box_score__home_team_stats__assists', 'apg')


def team_rpg(teams):
    """Rebounds Per Game"""
    return calculate_stat(teams, 'box_score__visitor_team_stats__total_rebounds',
                          'box_score__home_team_stats__total_rebounds', 'rpg')


def team_bpg(teams):
    """Blocks Per Game"""
    return calculate_stat(teams, 'box_score__visitor_team_stats__blocks', 'box_score__home_team_stats__blocks', 'bpg')


def team_spg(teams):
    """Steals Per Game"""
    return calculate_stat(teams, 'box_score__visitor_team_stats__steals', 'box_score__home_team_stats__steals', 'spg')


def team_fgp(teams):
    """Field goals percentage"""
    return calculate_stat(teams, 'box_score__visitor_team_stats__field_goals_percentage',
                          'box_score__home_team_stats__field_goals_percentage', 'fgp', 100)


def team_3fg(teams):
    """Three pointers made"""
    team_3fg_data = []
    for team in teams:
        visitor_games = get_games(team, is_home=False)
        home_games = get_games(team, is_home=True)

        visitor_three_pointers = visitor_games.aggregate(
            total=Sum('box_score__visitor_team_stats__three_point_field_goals'))['total']
        home_three_pointers = home_games.aggregate(
            total=Sum('box_score__home_team_stats__three_point_field_goals'))['total']

        total_three_pointers = visitor_three_pointers + home_three_pointers

        team_3fg_data.append({
            'team': team.name,
            '3fg': round(total_three_pointers, 1)
        })
    return sorted(team_3fg_data, key=lambda x: x['3fg'], reverse=True)[:5]


def team_3fgp(teams):
    """Three point percentage"""
    return calculate_stat(teams, 'box_score__visitor_team_stats__three_point_field_goals_percentage',
                          'box_score__home_team_stats__three_point_field_goals_percentage', '3fgp', 100)


def team_ftp(teams):
    """Free throw percentage"""
    return calculate_stat(teams, 'box_score__visitor_team_stats__free_throw_percentage',
                          'box_score__home_team_stats__free_throw_percentage', 'ftp', 100)


def get_stats(teams):
    team_stats = [{
        'Points Per Game': team_ppg(teams),
        'Assists Per Game': team_apg(teams),
        'Rebounds Per Game': team_rpg(teams),
        'Blocks Per Game': team_bpg(teams),
        'Steals Per Game': team_spg(teams),
        'Field Goal Percentage': team_fgp(teams),
        'Three Pointers Made': team_3fg(teams),
        'Three Point Percentage': team_3fgp(teams),
        'Free Throw Percentage': team_ftp(teams)
    }]
    return team_stats
