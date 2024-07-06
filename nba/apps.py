from django.apps import AppConfig


class NBAConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nba'

    def ready(self):
        import nba.signals
