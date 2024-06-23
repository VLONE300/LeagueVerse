from django.db.models import Avg


def get_games(model, team, is_home):
    """Get regular season home and away games"""
    field_name = 'home_team' if is_home else 'visitor_team'
    return model.objects.filter(**{field_name: team, 'type': 'Regular Season'})


def calculate_stat(model, teams, visitor_stat, home_stat, multiplier=1):
    """Calculate the average statistic and return the top 5 teams by value"""
    stat_data = []
    for team in teams:
        visitor_games = get_games(model, team, is_home=False)
        home_games = get_games(model, team, is_home=True)

        visitor_value = visitor_games.aggregate(avg_value=Avg(visitor_stat))['avg_value']
        home_value = home_games.aggregate(avg_value=Avg(home_stat))['avg_value']

        avg_stat = ((visitor_value + home_value) / 2) * multiplier

        stat_data.append({
            'team': team.name,
            'value': round(avg_stat, 1)
        })
    return sorted(stat_data, key=lambda x: x['value'], reverse=True)[:5]
