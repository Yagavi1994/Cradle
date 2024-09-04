from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    Configuration for the Blog app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        """
        Import signals when the app is ready.
        """
        import blog.signals
