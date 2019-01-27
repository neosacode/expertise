from django.apps import AppConfig


class Config(AppConfig):
    name = 'apps.core'
    verbose_name = "Core"

    def ready(self):
        import apps.core.signals
