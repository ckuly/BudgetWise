from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    month = models.PositiveSmallIntegerField(default=1)
    year = models.PositiveSmallIntegerField(default=2004)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def transactions_total(self):
        return Transaction.objects.filter(
            user=self.user,
            type="expense",
            date__year=self.year,
            date__month=self.month
        ).aggregate(total=models.Sum('amount'))['total'] or 0

    @property
    def is_surpassed(self):
        return self.transactions_total > self.amount

    class Meta:
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"

    def __str__(self):
        return f"Budget - {self.amount} ({self.month}/{self.year})"


class Transaction(models.Model):
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

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.type.capitalize()} - {self.amount} ({self.category.name})"  # NOQA


class SavingsGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    transactions = models.ManyToManyField(Transaction, related_name='savings_goals', blank=True)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def saved_amount(self):
        return sum(transaction.amount for transaction in self.transactions.all())  # NOQA

    def has_reached_goal(self):
        return self.saved_amount >= self.target_amount  # NOQA

    class Meta:
        verbose_name = "Saving Goal"
        verbose_name_plural = "Saving Goals"

    def __str__(self):
        return f"{self.name} - {self.saved_amount}/{self.target_amount}"


class Profile(models.Model):
    CURRENCIES = [
        ("USD", "Dollar"),
        ("EUR", "Euro"),
        ("JPY", "Japanese Yen"),
        ("GBP", "Pound Sterling"),
    ]

    PLANS = [
        ("free", "Free"),
        ("premium", "Premium"),
        ("elite", "Elite"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default="USD")
    timezone = models.CharField(max_length=50, default="UTC")
    profile_picture = models.ImageField(upload_to="profile_pictures/", default="profile_pictures/default.png")
    plan = models.CharField(max_length=10, choices=PLANS, default="free")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"Profile of {self.user.username}"  # NOQA


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"  # NOQA


class Update(models.Model):
    version = models.CharField(max_length=20, help_text="Version number (e.g., v1.0.0)")
    description = models.TextField(help_text="Description of the update")
    release_date = models.DateField(help_text="Release date of the update")

    class Meta:
        verbose_name = "Update"
        verbose_name_plural = "Updates"

    def __str__(self):
        return f"{self.version} - {self.release_date}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
