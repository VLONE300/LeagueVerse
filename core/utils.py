from asgiref.sync import sync_to_async
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


@sync_to_async
def delete_unrelated_box_scores(game, box_score):
    related_box_scores = game.objects.filter(box_score__isnull=False).values_list('box_score_id', flat=True)
    unrelated_box_scores = box_score.objects.exclude(id__in=related_box_scores)
    unrelated_box_scores.delete()


@sync_to_async
def delete_unrelated_team_stats(box_score, team_stats):
    related_team_stats = box_score.objects.values_list('home_team_stats_id', 'visitor_team_stats_id')
    related_team_stats_ids = set([item for sublist in related_team_stats for item in sublist])
    unrelated_team_stats = team_stats.objects.exclude(id__in=related_team_stats_ids)
    unrelated_team_stats.delete()


async def save_box_score(box_score, visitor_team_stats, home_team_stats):
    box_score = await sync_to_async(box_score.objects.create)(
        visitor_team_stats=visitor_team_stats,
        home_team_stats=home_team_stats
    )
    return box_score


async def save_team_stats(team_stats, stats):
    visitor_team_stats = await sync_to_async(team_stats.objects.create)(**stats[0])
    home_team_stats = await sync_to_async(team_stats.objects.create)(**stats[1])
    return visitor_team_stats, home_team_stats


async def is_game_exist(game, date_game, visitor_team, home_team):
    match_exists = await sync_to_async(
        game.objects.filter(
            date=date_game,
            visitor_team=visitor_team,
            visitor_pts__isnull=False,
            home_team=home_team,
            home_pts__isnull=False,
            box_score__isnull=False,
            status='Finished'
        ).exists)()
    return match_exists
