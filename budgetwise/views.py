from django.shortcuts import render
from budgetwise.models import Transaction, Category, Budget, SavingsGoal, Profile, Notification, AuditLog, Update


def index(request):
    transactions = Transaction.objects.all()
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    context = {
        'transactions': transactions,
        "num_visits": num_visits,
    }

    return render(request, "index.html", context)

def updates(request):
    all_updates = Update.objects.order_by("-release_date")
    latest_update = all_updates.first()
    archived_updates = all_updates[1:]

    context = {
        "latest_update": latest_update,
        "archived_updates": archived_updates,
    }
    return render(request, "updates.html", context)

def contacts(request):
    context = {}
    return render(request, "contacts.html", context)

def register(request):
    context = {}
    return render(request, "register.html", context)

def login(request):
    context = {}
    return render(request, "registration/login.html", context)

def profile(request):
    context = {}
    return render(request, "profile.html", context)

def dashboard(request):
    categories = Category.objects.all()
    budgets = Budget.objects.all()
    transactions = Transaction.objects.all()
    savings_goals = SavingsGoal.objects.all()
    profiles = Profile.objects.all()
    notifications = Notification.objects.filter(user=request.user, is_read=False) if request.user.is_authenticated else []
    audit_logs = AuditLog.objects.all()

    context = {
        "categories": categories,
        "budgets": budgets,
        "transactions": transactions,
        "savings_goals": savings_goals,
        "profiles": profiles,
        "notifications": notifications,
        "audit_logs": audit_logs,
    }

    return render(request, "dashboard.html", context)

def analytics(request):
    context = {}
    return render(request, "analytics.html", context)

def newsletter(request):
    context = {}
    return render(request, "newsletter.html", context)