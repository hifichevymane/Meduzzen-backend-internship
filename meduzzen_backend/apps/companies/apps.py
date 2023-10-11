from django.apps import AppConfig


class CompaniesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'companies'

    def ready(self):
        # Need for signals to work
        import companies.signals  #noqa: F401
