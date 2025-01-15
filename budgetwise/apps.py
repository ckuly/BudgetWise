from django.apps import AppConfig


class BudgetwiseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "budgetwise"

    def ready(self):
        import budgetwise.signals  # NOQA
