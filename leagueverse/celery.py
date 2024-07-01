import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leagueverse.settings')

app = Celery('leagueverse')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(['core.tasks'])

app.conf.beat_schedule = {
    'save-nba-standings-every-two-hours': {
        'task': 'core.tasks.save_nba_standings',
        'schedule': crontab(minute="0", hour='*/1'),
    },
    'save-nhl-standings-every-two-hours': {
        'task': 'core.tasks.save_nhl_standings',
        'schedule': crontab(minute="0", hour='*/1'),
    },

    'parse-nba-games-every-two-hours': {
        'task': 'core.tasks.parse_nba_games',
        'schedule': crontab(minute="0", hour='*/1'),
    },
    'parse-nhl-games-every-two-hours': {
        'task': 'core.tasks.parse_nhl_games',
        'schedule': crontab(minute="0", hour='*/1'),
    },
}
