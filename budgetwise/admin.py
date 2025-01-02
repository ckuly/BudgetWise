from django.contrib import admin
from .models import Category, Budget, Transaction, SavingsGoal, Profile, Notification, AuditLog


class CategoryAdmin(admin.ModelAdmin):
    pass


class BudgetAdmin(admin.ModelAdmin):
    pass


class TransactionAdmin(admin.ModelAdmin):
    pass


class SavingsAdmin(admin.ModelAdmin):
    pass


class ProfileAdmin(admin.ModelAdmin):
    pass


class NotificationAdmin(admin.ModelAdmin):
    pass


class AuditLogAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(Transaction)
admin.site.register(SavingsGoal)
admin.site.register(Profile)
admin.site.register(Notification)
admin.site.register(AuditLog)
