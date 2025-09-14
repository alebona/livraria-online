from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    """ Importa signals ao iniciar o app """
    def ready(self):
        import core.signals
