from django.apps import AppConfig


class SiyyanaAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'siyyana_app'

    def ready(self):
        import siyyana_app.signals  # Import the signals when the app is ready



