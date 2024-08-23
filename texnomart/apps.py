from django.apps import AppConfig


class TexnomartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'texnomart'

    def ready(self):
        import texnomart.signals
