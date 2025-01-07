from django.contrib import admin
from .models import Category, Budget, Transaction, SavingsGoal, Profile, Notification, AuditLog, Update


class CategoryAdmin(admin.ModelAdmin):
    pass


class BudgetAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "amount", "category", "created_at", "updated_at")
    list_editable = ("amount", "type", "category")
    list_filter = ("user", "type", "category")
    search_fields = ("user__username",)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "amount", "category", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("user", "type", "category")
    list_editable = ("amount", "type", "category")
    search_fields = ("user__username", "description")

    fieldsets = (
        ("General", {"fields": ("user", "type", "category", "amount", "description")}),
        ("Time", {"fields": ("date", "created_at", "updated_at",)}),
    )


class SavingsAdmin(admin.ModelAdmin):
    pass


class ProfileAdmin(admin.ModelAdmin):
    pass


class NotificationAdmin(admin.ModelAdmin):
    pass


class AuditLogAdmin(admin.ModelAdmin):
    pass


class UpdateAdmin(admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(SavingsGoal, SavingsAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(AuditLog, AuditLogAdmin)
admin.site.register(Update, UpdateAdmin)

# truksta inlines kuriu reiketu.