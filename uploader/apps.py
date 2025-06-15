from django.apps import AppConfig


class UploaderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "uploader"

    def ready(self):
        # Import template tags when the app is ready
        from django.template.defaulttags import register
        try:
            from .templatetags import custom_filters
        except ImportError:
            pass
