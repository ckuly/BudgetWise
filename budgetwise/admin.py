from django.contrib import admin
from .models import Category, Budget, Transaction, SavingsGoal, Profile, Notification, Update, ContactMessage


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at",)
    ordering = ("id",)


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
    list_display = ("id", "user", "name", "target_amount", "saved_amount", "due_date", "created_at")
    readonly_fields = ("created_at", "progress_percentage")
    list_filter = ("user", "due_date", "created_at")
    search_fields = ("name", "user__username")
    ordering = ("-due_date",)
    fieldsets = (
        ("General", {"fields": ("user", "name", "target_amount", "saved_amount", "transactions", "due_date")}),
        ("Progress and Timestamps", {"fields": ("progress_percentage", "created_at")}),
    )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "currency", "timezone", "plan", "created_at")
    readonly_fields = ("created_at",)
    list_filter = ("currency", "plan", "created_at")
    search_fields = ("user__username",)
    ordering = ("user__username",)
    fieldsets = (
        ("General", {"fields": ("user", "currency", "timezone", "plan")}),
        ("Profile Picture", {"fields": ("profile_picture",)}),
        ("Timestamps", {"fields": ("created_at",)}),
    )


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "is_read", "created_at")
    list_editable = ("is_read",)
    readonly_fields = ("created_at",)
    list_filter = ("user", "is_read", "created_at")
    search_fields = ("user__username", "message")
    ordering = ("-created_at",)


class UpdateAdmin(admin.ModelAdmin):
    list_display = ("id", "version", "release_date", "description")
    readonly_fields = ("release_date",)
    search_fields = ("version", "description")
    ordering = ("-release_date",)
    fieldsets = (
        ("Details", {"fields": ("version", "description")}),
        ("Release Information", {"fields": ("release_date",)}),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(SavingsGoal, SavingsAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Update, UpdateAdmin)
