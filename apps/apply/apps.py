from django.apps import AppConfig


class ApplyConfig(AppConfig):
    name = 'apps.apply'
    def ready(self):
        import apply.signals