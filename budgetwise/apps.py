from django.apps import AppConfig


class BudgetwiseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'budgetwise'

    def ready(self):
        from .signals import update_savings_goal_saved_amount_on_transaction_save, update_savings_goal_saved_amount_on_transaction_change