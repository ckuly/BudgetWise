from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import SavingsGoal, Transaction, Profile, Notification


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):  # NOQA
    if created:
        Profile.objects.create(user=instance)  # NOQA
        print('KWARGS: ', kwargs)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):  # NOQA
    instance.profile.save()


@receiver(m2m_changed, sender=SavingsGoal.transactions.through)
def update_savings_goal_saved_amount_on_transaction_change(sender, instance, action, **kwargs):  # NOQA
    if action in ['post_add', 'post_remove']:
        instance.refresh_from_db()
        total_saved_amount = instance.transactions.aggregate(Sum('amount'))['amount__sum'] or 0

        if instance.saved_amount != total_saved_amount:
            instance.saved_amount = total_saved_amount
            instance.save(update_fields=['saved_amount'])


@receiver(post_save, sender=Transaction)
def update_savings_goal_saved_amount_on_transaction_save(sender, instance, created, **kwargs):  # NOQA
    if instance.savings_goals.exists():
        for savings_goal in instance.savings_goals.all():
            total_saved_amount = savings_goal.transactions.aggregate(Sum('amount'))['amount__sum'] or 0
            if savings_goal.saved_amount != total_saved_amount:
                savings_goal.saved_amount = total_saved_amount
                savings_goal.save(update_fields=['saved_amount'])


@receiver(m2m_changed, sender=SavingsGoal.transactions.through)
def notify_goal_reached(sender, instance, action, **kwargs):  # NOQA
    if action == 'post_add':
        if instance.has_reached_goal():
            if not Notification.objects.filter(  # NOQA
                    user=instance.user,
                    message__icontains=f"Savings goal '{instance.name}' reached"
            ).exists():
                Notification.objects.create(  # NOQA
                    user=instance.user,
                    message=f"Congratulations! Your savings goal '{instance.name}' has been reached!"
                )
