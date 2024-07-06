from django.apps import AppConfig


class NHLConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nhl'

    def ready(self):
        import nhl.signals
