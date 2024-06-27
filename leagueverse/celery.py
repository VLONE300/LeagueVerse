import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leagueverse.settings')

app = Celery('leagueverse')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(['parsers.nba.tasks', 'parsers.nhl.tasks'])

app.conf.beat_schedule = {
    'save-nba-standings-every-hour': {
        'task': 'parsers.nba.tasks.save_nba_standings',
        'schedule': crontab(minute='0', hour='*/2'),
    },
    'save-nhl-standings-every-hour': {
        'task': 'parsers.nhl.tasks.save_nhl_standings',
        'schedule': crontab(minute='0', hour='*/2'),
    },
    'parse-nba-games-every-hour': {
        'task': 'parsers.nba.tasks.parse_nba_games',
        'schedule': crontab(minute='0', hour='*/2'),
    },
    'parse-nhl-games-every-hour': {
        'task': 'parsers.nhl.tasks.parse_nhl_games',
        'schedule': crontab(minute='0', hour='*/1'),
    },
}
