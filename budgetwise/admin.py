from django.contrib import admin
from .models import Category, Budget, Transaction, SavingsGoal, Profile, Notification, AuditLog

admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(Transaction)
admin.site.register(SavingsGoal)
admin.site.register(Profile)
admin.site.register(Notification)
admin.site.register(AuditLog)
