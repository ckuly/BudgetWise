from django.apps import AppConfig


class BudgetwiseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'budgetwise'

    def ready(self):
        from .signals import create_user_profile, save_user_profile # NOQA