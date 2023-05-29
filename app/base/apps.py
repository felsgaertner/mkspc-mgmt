from django.apps import AppConfig


class AppBaseConfig(AppConfig):
    name = 'app.base'

    def ready(self):
        import app.base.signals
