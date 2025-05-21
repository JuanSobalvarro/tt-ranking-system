from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        import profiles.signals
        # Import the signals module to ensure that the signals are registered when the app is ready.
        # This is necessary to ensure that the signals are connected when the app is loaded.
