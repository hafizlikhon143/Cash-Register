from django.apps import AppConfig


class AppViewConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_view'
    
    def ready(self):
        import app_view.signals
