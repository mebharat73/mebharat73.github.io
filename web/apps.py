from django.apps import AppConfig

class WebAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Default field type for auto-incrementing primary keys
    name = 'web'  # The name of your application
    verbose_name = 'Web Application'  # A human-readable name for the application (optional)

    def ready(self):
        # This method is called when the application is ready.
        # You can put any startup logic here, such as signal registration.
        pass