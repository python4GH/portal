from django.apps import AppConfig


class TrisolaceConfig(AppConfig):
    name = 'trisolace'

    def ready(self):
        import trisolace.signals
