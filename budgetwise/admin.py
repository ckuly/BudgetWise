from django.contrib import admin
from .models import Category, Budget, Transaction, SavingsGoal, Profile, Notification, Update, ContactMessage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    readonly_fields = ("created_at",)
    ordering = ("id",)
    list_per_page = 20


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "created_at")
    list_editable = ("amount",)
    search_fields = ("user__username",)
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("user",)
    list_filter = ("user", "created_at")
    ordering = ("-created_at",)
    list_per_page = 20


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type", "amount", "category", "date")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("user__username", "description", "category__name")
    autocomplete_fields = ("user", "category")
    list_filter = ("type", "category", "date")
    ordering = ("-date",)
    list_per_page = 25


@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "target_amount", "saved_amount", "due_date")
    readonly_fields = ("created_at", "saved_amount")
    autocomplete_fields = ("user",)
    filter_horizontal = ("transactions",)
    search_fields = ("name", "user__username")
    list_filter = ("user", "due_date", "created_at")
    ordering = ("-due_date",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "currency", "plan", "created_at")
    readonly_fields = ("created_at",)
    search_fields = ("user__username",)
    list_filter = ("currency", "plan")
    ordering = ("user__username",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "short_message", "is_read", "created_at")
    list_editable = ("is_read",)
    readonly_fields = ("created_at",)
    search_fields = ("user__username", "message")
    list_filter = ("is_read", "created_at")
    ordering = ("-created_at",)

    @staticmethod
    def short_message(obj):
        return obj.message[:50]


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ("id", "version", "release_date", "release_date")
    search_fields = ("version", "description")
    ordering = ("-release_date",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "short_message", "created_at")
    readonly_fields = ("created_at",)
    search_fields = ("name", "email", "message")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

    @staticmethod
    def short_message(obj):
        return obj.message[:50]
