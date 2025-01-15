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
    list_display = ("id", "user", "amount", "created_at", "updated_at")
    list_editable = ("amount",)
    list_filter = ("user", "created_at")
    search_fields = ("user__username",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    autocomplete_fields = ("user",)
    fieldsets = (
        ("General Information", {
            "fields": ("user", "amount", "description"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type", "amount", "category", "date", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("type", "category", "date", "created_at")
    search_fields = ("user__username", "description", "category__name")
    ordering = ("-date",)
    autocomplete_fields = ("user", "category")
    fieldsets = (
        ("Transaction Details", {
            "fields": ("user", "type", "category", "amount", "description"),
        }),
        ("Date and Timestamps", {
            "fields": ("date", "created_at", "updated_at"),
        }),
    )
    list_per_page = 25


@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user", "name", "target_amount", "saved_amount", "progress_percentage", "due_date", "created_at")
    readonly_fields = ("created_at", "saved_amount", "progress_percentage")
    list_filter = ("user", "due_date", "created_at")
    search_fields = ("name", "user__username")
    ordering = ("-due_date",)
    autocomplete_fields = ("user",)
    filter_horizontal = ("transactions",)
    fieldsets = (
        ("Savings Goal Details", {
            "fields": ("user", "name", "target_amount", "due_date"),
        }),
        ("Transactions", {
            "fields": ("transactions",),
        }),
        ("Progress and Timestamps", {
            "fields": ("saved_amount", "progress_percentage", "created_at"),
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "currency", "timezone", "plan", "created_at")
    readonly_fields = ("created_at",)
    list_filter = ("currency", "plan", "created_at")
    search_fields = ("user__username",)
    ordering = ("user__username",)
    fieldsets = (
        ("Profile Details", {
            "fields": ("user", "currency", "timezone", "plan"),
        }),
        ("Profile Picture", {
            "fields": ("profile_picture",),
        }),
        ("Timestamps", {
            "fields": ("created_at",),
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "short_message", "is_read", "created_at")
    list_editable = ("is_read",)
    readonly_fields = ("created_at",)
    list_filter = ("user", "is_read", "created_at")
    search_fields = ("user__username", "message")
    ordering = ("-created_at",)
    list_per_page = 25

    def short_message(self, obj):
        return obj.message[:50]

    short_message.short_description = "Message"


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ("id", "version", "release_date", "description")
    readonly_fields = ("release_date",)
    search_fields = ("version", "description")
    ordering = ("-release_date",)
    fieldsets = (
        ("Update Details", {
            "fields": ("version", "description"),
        }),
        ("Release Date", {
            "fields": ("release_date",),
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "short_message", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    def short_message(self, obj):
        return obj.message[:50]

    short_message.short_description = "Message"
