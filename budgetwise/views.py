from django.shortcuts import render
from budgetwise.models import Transaction, Category, Budget, SavingsGoal, Profile, Notification, AuditLog


def index(request):
    transactions = Transaction.objects.all()
    context = {'transactions': transactions}
    return render(request, 'index.html', context)

def dashboard(request):
    categories = Category.objects.all()
    budgets = Budget.objects.all()
    transactions = Transaction.objects.all()
    savings_goals = SavingsGoal.objects.all()
    profiles = Profile.objects.all()
    notifications = Notification.objects.filter(user=request.user, is_read=False) if request.user.is_authenticated else []
    audit_logs = AuditLog.objects.all()

    context = {
        'categories': categories,
        'budgets': budgets,
        'transactions': transactions,
        'savings_goals': savings_goals,
        'profiles': profiles,
        'notifications': notifications,
        'audit_logs': audit_logs,
    }

    return render(request, 'dashboard.html', context)