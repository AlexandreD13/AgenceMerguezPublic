from django.apps import AppConfig

from agence import settings


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        from agence.container import Container
        container = Container()
        container.config.from_dict(settings.__dict__)
        container.wire(modules=['.tasks', '.models','.views'])
