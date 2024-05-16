import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'leagueverse.settings')

app = Celery('leagueverse')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'save-nba-standings-every-five-minutes': {
        'task': 'parsers.tasks.save_nba_standings',
        'schedule': crontab(minute='*/5'),  # Запускать каждые 5 минут
    },
}