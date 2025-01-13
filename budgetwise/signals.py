from django.db.models import Sum
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import SavingsGoal, Transaction


# Signal to handle updates on transaction changes
@receiver(m2m_changed, sender=SavingsGoal.transactions.through)
def update_savings_goal_saved_amount_on_transaction_change(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove']:
        # When transactions are added or removed, we need to update the saved_amount
        instance.refresh_from_db()  # Ensure we're working with the latest instance
        total_saved_amount = instance.transactions.aggregate(Sum('amount'))['amount__sum'] or 0

        if instance.saved_amount != total_saved_amount:
            instance.saved_amount = total_saved_amount
            instance.save(update_fields=['saved_amount'])


# Signal for the Transaction model to handle updates when a transaction is saved
@receiver(post_save, sender=Transaction)
def update_savings_goal_saved_amount_on_transaction_save(sender, instance, created, **kwargs):
    if instance.savings_goals.exists():
        for savings_goal in instance.savings_goals.all():
            total_saved_amount = savings_goal.transactions.aggregate(Sum('amount'))['amount__sum'] or 0
            if savings_goal.saved_amount != total_saved_amount:
                savings_goal.saved_amount = total_saved_amount
                savings_goal.save(update_fields=['saved_amount'])
