from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import SavingsGoal, Transaction, Profile, Notification

@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs): # NOQA
    """Create or save a user profile on user creation or update."""
    if created:
        Profile.objects.create(user=instance) # NOQA
    else:
        instance.profile.save()

@receiver(m2m_changed, sender=SavingsGoal.transactions.through)
def update_savings_goal(sender, instance, action, **kwargs): # NOQA
    """Update the saved amount and notify if the goal is reached."""
    if action in ['post_add', 'post_remove']:
        total_saved = instance.transactions.aggregate(Sum('amount'))['amount__sum'] or 0
        if instance.saved_amount != total_saved:
            instance.saved_amount = total_saved
            instance.save(update_fields=['saved_amount'])

        if action == 'post_add' and instance.has_reached_goal():
            Notification.objects.get_or_create( # NOQA
                user=instance.user,
                message=f"Congratulations! Your savings goal '{instance.name}' has been reached!"
            )

@receiver(post_save, sender=Transaction)
def update_related_savings_goals(sender, instance, **kwargs): # NOQA
    """Recalculate saved amounts for associated savings goals."""
    for goal in instance.savings_goals.all():
        total_saved = goal.transactions.aggregate(Sum('amount'))['amount__sum'] or 0
        if goal.saved_amount != total_saved:
            goal.saved_amount = total_saved
            goal.save(update_fields=['saved_amount'])
