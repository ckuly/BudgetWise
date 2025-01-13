from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    """Categories explanation here"""
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Budget(models.Model):
    """Budgets explanation here"""
    CATEGORY_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=CATEGORY_TYPES, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name} - {self.amount}"


class Transaction(models.Model):
    """Transaction explanation here"""
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type.capitalize()} - {self.amount} ({self.category.name})"


class SavingsGoal(models.Model):
    """Saving goals explanation here"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    saved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    transactions = models.ManyToManyField(Transaction, related_name='savings_goals', blank=True)

    @property
    def progress_percentage(self):
        return (self.saved_amount / self.target_amount) * 100 if self.target_amount > 0 else 0

    class Meta:
        verbose_name = "Saving Goal"
        verbose_name_plural = 'Saving Goals'

    def __str__(self):
        return f"{self.name} - {self.saved_amount}/{self.target_amount}"


class Profile(models.Model):
    """Profile explanation here"""
    CURRENCIES = [
        ('USD', 'Dollar'),
        ('EUR', 'Euro'),
        ('JPY', 'Japanese Yen'),
        ('GBP', 'Pound Sterling'),
    ]

    PLANS = [
        ('free', 'Free'),
        ('premium', 'Premium'),
        ('elite', 'Elite'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default="USD")
    timezone = models.CharField(max_length=50, default="UTC")
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg')
    plan = models.CharField(max_length=10, choices=PLANS, default="free")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f"Profile of {self.user.username}"


class Notification(models.Model):
    """Notification explanation here"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"


class Update(models.Model):
    """Update explanation here"""
    version = models.CharField(max_length=20, help_text="Version number (e.g., v1.0.0)")
    description = models.TextField(help_text="Description of the update")
    release_date = models.DateField(help_text="Release date of the update")

    def __str__(self):
        return f"{self.version} - {self.release_date}"
