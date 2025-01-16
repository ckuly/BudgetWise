from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic import CreateView, ListView
from budgetwise.models import Transaction, Budget, SavingsGoal, Notification, Update, Profile, Category, ContactMessage
import calendar
from django.utils.timezone import now
from .utils import generate_monthly_chart


def index(request):
    transactions = Transaction.objects.all()  # NOQA
    total_members = User.objects.count()
    paid_members = Profile.objects.filter(plan__in=["premium", "elite"]).count()  # NOQA

    context = {
        "total_members": total_members,
        "paid_members": paid_members,
        "transactions": transactions,
    }

    return render(request, "index.html", context)


def updates(request):
    all_updates = Update.objects.order_by("-release_date")  # NOQA
    latest_update = all_updates.first()
    archived_updates = all_updates[1:]

    context = {
        "latest_update": latest_update,
        "archived_updates": archived_updates,
    }
    return render(request, "base/updates.html", context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        ContactMessage.objects.create(name=name, email=email, message=message)  # NOQA
        messages.success(request, "Your message has been received. We will get back to you soon!")

    return render(request, "base/contacts.html")


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'The username "{username}" is already taken!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'A user with the email "{email}" is already registered!')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'User "{username}" has been successfully registered!')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    return render(request, 'base/register.html')


def login(request):
    context = {}
    return render(request, "registration/login.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        profile = request.user.profile  # NOQA

        if 'remove_picture' in request.POST:
            if profile.profile_picture.name != 'profile_pictures/default.png':  # NOQA
                profile.profile_picture.delete(save=False)  # NOQA
            profile.profile_picture = 'profile_pictures/default.png'

        profile.currency = request.POST.get("currency", profile.currency)

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    context = {
        "user": request.user,
    }
    return render(request, "base/profile.html", context)


@login_required
def dashboard(request):
    user = request.user

    budgets = Budget.objects.filter(user=user)  # NOQA
    transactions = Transaction.objects.filter(user=user).order_by('-date')  # NOQA
    savings_goals = SavingsGoal.objects.filter(user=user)  # NOQA
    notifications = Notification.objects.filter(user=user, is_read=False)  # NOQA

    context = {
        "budgets": budgets,
        "transactions": transactions,
        "savings_goals": savings_goals,
        "profile": user.profile,
        "notifications": notifications,
    }

    return render(request, "base/dashboard.html", context)


@login_required
def analytics(request):
    user = request.user

    try:
        selected_year = int(request.GET.get('year', now().year))
    except ValueError:
        selected_year = now().year

    monthly_chart, monthly_net_data = generate_monthly_chart(user, selected_year)
    years = Transaction.objects.filter(user=user).dates('date', 'year', order='ASC')  # NOQA

    transactions_by_month = [
        {
            "month": calendar.month_name[month],
            "transactions": Transaction.objects.filter(  # NOQA
                user=user,
                date__year=selected_year,
                date__month=month
            ).order_by('date'),
        }
        for month in range(1, 13)
    ]

    context = {
        'monthly_chart': monthly_chart,
        'monthly_net_data': monthly_net_data,
        'selected_year': selected_year,
        'years': [year.year for year in years],
        'transactions_by_month': transactions_by_month,
    }

    return render(request, "base/analytics.html", context)


@login_required
def membership(request):
    return render(request, "base/membership.html")


@login_required
def change_plan(request, plan):
    valid_plans = ['free', 'premium', 'elite']
    if plan in valid_plans:
        profile = request.user.profile  # NOQA
        profile.plan = plan
        profile.save()
        messages.success(request, f"Your plan has been updated to {plan.capitalize()}!")
    else:
        messages.error(request, "Invalid plan selection.")
    return redirect('membership')


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'crud/transactions.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-date') # NOQA


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['category', 'type', 'amount', 'date', 'description']
    template_name = 'crud/transaction_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Transaction added successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return '/home/dashboard/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all() # NOQA
        return context


class SavingGoalCreateView(LoginRequiredMixin, CreateView):
    model = SavingsGoal
    fields = ['name', 'target_amount', 'due_date']
    template_name = 'crud/create_saving_goal.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Savings goal added successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return '/home/dashboard/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_transactions'] = Transaction.objects.filter(user=self.request.user).exclude( # NOQA
            savings_goals__isnull=False)
        return context


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    fields = ['amount', 'description', 'month', 'year']
    template_name = 'crud/create_budget.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Budget added successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return '/home/dashboard/'


@login_required
def budget_manage(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)

    if request.method == "POST":
        if "edit" in request.POST:
            try:
                budget.amount = float(request.POST["amount"])
                budget.description = request.POST["description"]
                budget.month = int(request.POST["month"])
                budget.year = int(request.POST["year"])
                budget.save()
                messages.success(request, "Budget updated successfully!")
            except ValueError:
                messages.error(request, "Invalid input.")
            return redirect("dashboard")

        elif "delete" in request.POST:
            budget.delete()
            messages.success(request, "Budget deleted successfully!")
            return redirect("dashboard")

    return render(request, "crud/budget_manage.html", {"budget": budget})


@login_required
def saving_goal_manage(request, saving_goal_id):
    saving_goal = get_object_or_404(SavingsGoal, id=saving_goal_id, user=request.user)

    if request.method == "POST":
        if "delete_goal" in request.POST:
            saving_goal.delete()
            messages.success(request, "Savings goal deleted successfully!")
            return redirect("dashboard")

        remove_ids = request.POST.getlist("remove_transactions")
        if remove_ids:
            transactions = Transaction.objects.filter(id__in=remove_ids, user=request.user) # NOQA
            saving_goal.transactions.remove(*transactions)
            messages.success(request, f"{len(transactions)} transaction(s) removed from the savings goal.")

        assign_ids = request.POST.getlist("assign_transactions")
        if assign_ids:
            transactions = Transaction.objects.filter(id__in=assign_ids, user=request.user, type="income") # NOQA
            saving_goal.transactions.add(*transactions)
            messages.success(request, f"{len(transactions)} transaction(s) assigned to the savings goal.")

        return redirect("dashboard")

    available_transactions = Transaction.objects.filter(user=request.user, type="income").exclude( # NOQA
        savings_goals=saving_goal)

    context = {
        "saving_goal": saving_goal,
        "available_transactions": available_transactions,
    }
    return render(request, "crud/saving_goal_manage.html", context)


@login_required
def transaction_manage(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)

    if request.method == 'POST':
        if 'edit' in request.POST:
            try:
                transaction.category_id = request.POST['category']
                transaction.amount = float(request.POST.get('amount', '0') or '0')
                transaction.description = request.POST['description']
                transaction.date = request.POST.get('date') or transaction.date
                transaction.save()
                messages.success(request, "Transaction updated successfully!")
                return redirect('dashboard')
            except ValueError as e:
                messages.error(request, f"Error: {e}")
            except Exception:
                messages.error(request, "An unexpected error occurred. Please try again.")

        elif 'delete' in request.POST:
            transaction.delete()
            messages.success(request, "Transaction deleted successfully!")
            return redirect('dashboard')

    context = {
        'transaction': transaction,
        'categories': Category.objects.all(), # NOQA
    }
    return render(request, 'crud/transaction_manage.html', context)


@login_required
def mark_all_notifications_as_read(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)  # NOQA
    notifications.update(is_read=True)
    messages.success(request, "All notifications marked as read.")
    return redirect('dashboard')
